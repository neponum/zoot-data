#!/usr/bin/env python3
"""Применяет канон из translation/ru_RU/glossary.json к CSV-переводам.

Правит ТОЛЬКО колонку Translation (строки line-N) и подписи char-N.
Колонки ID / Character / Original Text / Reference не трогает.

    python3 tools/apply_glossary.py a001              # dry-run
    python3 tools/apply_glossary.py a001 --apply
    python3 tools/apply_glossary.py all --apply --terms infected,knights_treasure
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"
GLOSSARY = LANG_DIR / "glossary.json"


def build_infected_replacer(spec: dict) -> callable:
    """Зараженн* → Инфицированн* с сохранением окончания (прилагательное)."""
    pattern = re.compile(spec["regex"])
    stem = spec["replace_stem"]

    def repl(m: re.Match) -> str:
        whole = m.group(0)
        # окончание = всё после основы «зараженн/заражённ/инфицированн»
        m2 = re.match(r"(?i)(зара?ж[её]нн|инфицированн)(.*)$", whole)
        if not m2:
            return whole
        return stem + m2.group(2)

    return lambda text: pattern.sub(repl, text)


def build_stem_replacer(spec: dict):
    """Основа + окончание: Казимира → Казимежа, Нирл → Ниарл."""
    pat = re.compile(spec["regex"])
    inner = re.compile(spec["stem_regex"])
    stem = spec["replace_stem"]

    def repl(m: re.Match) -> str:
        inner_match = inner.match(m.group(0))
        ending = inner_match.group(1) if inner_match and inner_match.lastindex else ""
        return stem + ending

    return lambda text: pat.sub(repl, text)


def apply_terms(text: str, terms: dict, enabled: set[str], counters: dict) -> str:
    for name, spec in terms.items():
        if name.startswith("_"):
            continue
        if enabled and name not in enabled:
            continue
        for src, dst in spec.get("fix_first", {}).items():
            if src in text:
                counters[name] = counters.get(name, 0) + text.count(src)
                text = text.replace(src, dst)
        if "map" in spec:
            for src, dst in spec["map"].items():
                if src == dst:
                    continue  # каноничная форма: замены нет, только фиксация вида
                if src in text:
                    counters[name] = counters.get(name, 0) + text.count(src)
                    text = text.replace(src, dst)
        if "regex" in spec and "stem_regex" in spec:
            repl = build_stem_replacer(spec)
            new = repl(text)
            if new != text:
                counters[name] = counters.get(name, 0) + len(re.findall(spec["regex"], text))
                text = new
        elif "regex" in spec and "replace_stem" in spec:
            repl = build_infected_replacer(spec)
            new = repl(text)
            if new != text:
                counters[name] = counters.get(name, 0) + len(re.findall(spec["regex"], text))
                text = new
    return text


MULTISPACE_RE = re.compile(r"\s{2,}")
# апостроф НЕ трогаем: он часть транслитерации (Хо'олхейак, Виш'адель)
QUOTE_CHARS_RE = re.compile(r"[«»„“”\"]")


def strip_label_quotes(label: str) -> str:
    """Тег говорящего — служебная подпись, кавычек в ней не бывает.

    «Капитан» → Капитан
    Охранник «Рая пропеллеров» → Охранник Рая пропеллеров
    «Клиффхэнгер» Клифф → Клиффхэнгер Клифф
    """
    cleaned = QUOTE_CHARS_RE.sub("", label)
    return MULTISPACE_RE.sub(" ", cleaned).strip()


CAP_LETTER_RE = re.compile(r"\s+([A-F])$")
# одиночная буква-суффикс в конце подписи: «Солдат Дублинна Б»
TRAILING_LETTER_RE = re.compile(r"\s+[A-Za-zА-Яа-яЁё]$")
CAP_MAP = {"A": "А", "B": "Б", "C": "В", "D": "Г", "E": "Д", "F": "Е"}
ASSET_ID_RE = re.compile(r"^(avg_|char_\d|npc_|char_[a-z])", re.I)
CJK_RE = re.compile(r"[\u3000-\u9fff]")


def cyrillic_cap_suffix(label: str) -> str:
    """«Адаклис B» → «Адаклис Б». Латинские Rhine Lab / Blacksteel не трогаем."""
    m = CAP_LETTER_RE.search(label)
    return label[: m.start(1)] + CAP_MAP[m.group(1)] if m else label


def collect_cjk_variants() -> dict[str, str]:
    """CN-подпись → самая частая русская подпись (majority vote)."""
    votes: dict[str, dict[str, int]] = {}
    for path in sorted(LANG_DIR.glob("*/*.csv")):
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                if len(row) < 5 or not row[0].startswith("char-"):
                    continue
                cn, ru = row[1].strip(), row[4].strip()
                if cn and ru and not CJK_RE.search(ru):
                    votes.setdefault(cn, {})
                    votes[cn][ru] = votes[cn].get(ru, 0) + 1
    return {
        cn: max(counts.items(), key=lambda kv: kv[1])[0]
        for cn, counts in votes.items()
        if len(counts) == 1 or list(counts.values()).count(max(counts.values())) == 1
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="папка эпизода или all")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--terms", help="через запятую: infected,knights_treasure,village_dewville,surzahar_language")
    ap.add_argument("--names", action="store_true", help="применять реестр подписей char-N")
    ap.add_argument("--unquote", action="store_true", help="снимать лапки с целого тега: «Капитан» → Капитан")
    ap.add_argument("--cap-letters", action="store_true", help="латинские A-F в хвосте тега → кириллица")
    ap.add_argument("--asset-ids", action="store_true", help="ID ассетов (avg_…, char_…) → ???")
    ap.add_argument("--fix-cjk", action="store_true", help="китайский в RU-теге → канон или majority vote")
    ap.add_argument("--limit", type=int, default=0, help="показать не больше N примеров на правило")
    args = ap.parse_args()

    gloss = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    terms = gloss["terms"]
    names = {**gloss["names"].get("npc_labels", {}), **gloss["names"]["entries"]}
    # пометка «?» — только для реестра предположений, в данные не попадает
    names = {k: (v[:-1] if v.endswith("?") else v) for k, v in names.items()}
    enabled = {t.strip() for t in args.terms.split(",") if t.strip()} if args.terms else set()

    dirs = (
        sorted(p for p in LANG_DIR.iterdir() if p.is_dir())
        if "all" in args.targets
        else [LANG_DIR / t for t in args.targets]
    )

    counters: dict[str, int] = {}
    name_changes: list[str] = []
    cap_changes: list[str] = []
    asset_changes: list[str] = []
    cjk_changes: list[str] = []
    cjk_variants = collect_cjk_variants() if args.fix_cjk else {}
    unverified: list[str] = []
    unquote_changes: list[str] = []
    files_touched = 0

    for d in dirs:
        if not d.is_dir():
            print(f"Нет папки: {d}", file=sys.stderr)
            return 2
        for path in sorted(d.glob("*.csv")):
            text = path.read_text(encoding="utf-8", newline="")
            eol = "\r\n" if "\r\n" in text else "\n"
            lines = text.splitlines(keepends=True)
            reader = csv.reader(lines)
            out: list[str] = []
            start = 0
            changed = False

            for row in reader:
                end = reader.line_num
                raw = "".join(lines[start:end])
                start = end

                if len(row) >= 5 and row[0].startswith("__"):
                    out.append(raw)
                    continue

                new_row = list(row)
                if row and row[0].startswith("char-"):
                    cn, original = row[1], row[4]
                    label = original
                    tag = f"{path.parent.name}/{path.name} {row[0]}"

                    # 1. точный ключ реестра
                    if args.names and cn in names and names[cn] != label:
                        label = names[cn]
                        name_changes.append(f"{tag} {cn} → {label}")
                    else:
                        # 2. 深池士兵A → базовая запись 深池士兵 + буква-суффикс
                        base = cn[:-1] if cn and cn[-1] in "ABCDEF" else ""
                        if cn not in names and base in names:
                            base_ru = names[base]
                            # «Солдат Дублинна» + B → «Солдат Дублинна Б»;
                            # «Солдат» + B → «Солдат Б»
                            canon = base_ru if TRAILING_LETTER_RE.search(base_ru) else f"{base_ru} {CAP_MAP[cn[-1]]}"
                            if canon != label:
                                name_changes.append(f"{tag} {cn} → {canon}")
                                label = canon

                        # 3. термины в подписи («Зараженный рыцарь» → «Инфицированный рыцарь»)
                        if enabled or True:
                            fixed = apply_terms(label, terms, enabled, counters)
                            if fixed != label:
                                label = fixed

                        # 4. чистка тега: кавычки, латинские буквы, ID ассетов
                        if args.unquote:
                            stripped = strip_label_quotes(label)
                            if stripped != label:
                                unquote_changes.append(f"{tag} {label} → {stripped}")
                                label = stripped
                        if args.cap_letters:
                            capped = cyrillic_cap_suffix(label)
                            if capped != label:
                                cap_changes.append(f"{tag} {label} → {capped}")
                                label = capped
                        if args.asset_ids and ASSET_ID_RE.match(label):
                            asset_changes.append(f"{tag} {label} → ???")
                            label = "???"

                        # 5. китайский в русском теге
                        if args.fix_cjk and CJK_RE.search(label):
                            canon = names.get(cn) or cjk_variants.get(cn)
                            if canon and canon != label:
                                if canon.endswith("?"):
                                    # перевод-предположение: в данные идёт без «?»,
                                    # а сам попадает в список на проверку
                                    unverified.append(f"{cn}\t{canon[:-1]}")
                                    canon = canon[:-1]
                                if cn and cn[-1] in "ABCDEF":
                                    canon = TRAILING_LETTER_RE.sub("", canon).rstrip() + " " + CAP_MAP[cn[-1]]
                                cjk_changes.append(f"{tag} {cn} {label} → {canon}")
                                label = canon

                    if label != original:
                        new_row[4] = label
                elif len(row) >= 5 and row[0].startswith("line-"):
                    new_row[4] = apply_terms(row[4], terms, enabled, counters)

                if new_row != row:
                    buf = io.StringIO()
                    csv.writer(buf, lineterminator=eol).writerow(new_row)
                    out.append(buf.getvalue())
                    changed = True
                else:
                    out.append(raw)

            if changed:
                files_touched += 1
                if args.apply:
                    with open(path, "w", encoding="utf-8", newline="") as fh:
                        fh.write("".join(out))

    def show(title: str, items: list[str]) -> None:
        limit = args.limit or 40
        print(f"\n{title}: {len(items)}")
        for s in items[:limit]:
            print("   ", s)
        if len(items) > limit:
            print(f"    … ещё {len(items) - limit}")

    if args.names:
        show("подписи char-N по реестру", name_changes)
    if args.unquote:
        show("лапки сняты с тега", unquote_changes)
    if args.cap_letters:
        show("латинские буквы → кириллица", cap_changes)
    if args.asset_ids:
        show("ID ассетов → ???", asset_changes)
    if args.fix_cjk:
        show("китайский в RU-теге исправлен", cjk_changes)
    if enabled or not args.names:
        print("\nтермины (замен):")
        for k, v in sorted(counters.items(), key=lambda kv: -kv[1]):
            print(f"    {k}: {v}")

    if unverified:
        review = REPO / "tools" / "npc_labels_review.md"
        body = "# Имена, переведённые по предположению — нужна проверка NUM\n\n"
        body += "Источник: `tools/npc_labels.py` (знак `?`).\n\n| CN | предположение |\n|---|---|\n"
        for line in sorted(set(unverified)):
            cn, ru = line.split("\t", 1)
            body += f"| {cn} | {ru} |\n"
        if args.apply:
            review.write_text(body, encoding="utf-8")
        print(f"\nна проверку: {len(set(unverified))} имён -> {review}")

    mode = "ПРИМЕНЕНО" if args.apply else "dry-run"
    print(f"\n{mode}: файлов затронуто {files_touched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())