#!/usr/bin/env python3
"""Сводит варианты подписей говорящих к одной форме, ориентируясь на EN.

Для каждой китайской подписи, у которой в переводах несколько русских форм,
выбирает одну:

  1. точный ключ реестра (glossary.json) — приоритет выше всего;
  2. для личных имён — вариант, ближайший по транслитерации к английскому
     имени из игровых данных (Closure → Кложер, не «Клоша»);
  3. для обобщённых ярлыков — вариант, чьи ключевые слова совпадают с EN
     (Dublinn Soldier → «Солдат Дублинна», не «Солдат Deepness»);
  4. при равенстве — самый частотный вариант.

    python3 tools/unify_labels.py                  # отчёт + dry-run
    python3 tools/unify_labels.py --md tools/UNIFY.md
    python3 tools/unify_labels.py --apply
"""

from __future__ import annotations

import argparse
import csv
import difflib
import os
import subprocess
import glob
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"
GLOSSARY = LANG_DIR / "glossary.json"

RU_EN = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu",
    "я": "ya",
}

# EN-ключевое слово → русское слово, по которому выбираем вариант ярлыка
KEYWORDS = {
    "soldier": "солдат", "mercenary": "наемник", "prisoner": "заключ", "citizen": "граждан",
    "civilian": "граждан", "worker": "рабоч", "guard": "страж", "officer": "офицер",
    "doctor": "врач", "woman": "женщин", "man": "мужчин", "girl": "девоч", "boy": "мальчик",
    "voice": "голос", "narrator": "рассказчик", "system": "система", "teacher": "учител",
    "merchant": "торгов", "thief": "вор", "criminal": "преступник", "demon": "демон",
    "merchant": "торгов", "knight": "рыцар", "mage": "маг", "priest": "священник",
    "priest": "жрец", "student": "студент", "patient": "больн", "doctor": "доктор",
    "miner": "шахтёр", "miner": "шахтер", "farmer": "фермер", "fisherman": "рыбак",
    "hunter": "охотник", "sailor": "матрос", "doctor": "врач", "child": "ребён",
    "elder": "стар", "operator": "оперативник", "rhodes": "родос", "soldier": "солдат",
}


def translit(ru: str) -> str:
    out = []
    for ch in ru.lower().replace("'", "").replace("’", ""):
        out.append(RU_EN.get(ch, ch))
    return "".join(out)


def norm_en(en: str) -> str:
    s = unicodedata.normalize("NFKD", en.lower())
    return re.sub(r"[^a-z]", "", s)


ROLE_CN = re.compile(
    r"士兵|战士|工人|商人|路人|平民|囚犯|猎人|干员|市民|居民|学生|病人|教师|"
    r"警察|守卫|警员|佣兵|囚|女孩|男孩|女性|男性|声音|群众|人群|村民|军官|"
    r"商人A|商人B|人们|民众"
)
ROLE_EN = re.compile(
    r"soldier|warrior|worker|merchant|passerby|civilian|prisoner|hunter|operator|"
    r"citizen|resident|student|patient|teacher|policeman|guard|mercenary|girl|boy|"
    r"woman|man|voice|crowd|villager|officer",
    re.I,
)


def is_generic(cn: str, en: str) -> bool:
    """Обобщённый ярлык толпы, а не имя собственное."""
    return bool(ROLE_CN.search(cn)) or bool(ROLE_EN.search(en or ""))


def similarity(ru: str, en: str) -> float:
    return difflib.SequenceMatcher(None, translit(ru), norm_en(en)).ratio()


def keyword_score(ru: str, en: str) -> int:
    en_words = set(re.findall(r"[a-z]+", en.lower()))
    ru_low = ru.lower().replace("ё", "е")
    score = 0
    for en_word in en_words:
        for key, ru_word in KEYWORDS.items():
            if key in en_word and ru_word in ru_low:
                score += 1
                break
    return score


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--md", default=str(REPO / "tools" / "UNIFY.md"))
    ap.add_argument("--top", type=int, default=60)
    ap.add_argument("--min-variants", type=int, default=2)
    ap.add_argument("--baseline-git", action="store_true",
                    help="считать варианты по исходной версии (git index), а не по текущим файлам")
    args = ap.parse_args()

    gloss = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    registry = {**gloss["names"].get("npc_labels", {}), **gloss["names"]["entries"]}
    for key in list(registry):
        registry[key] = registry[key].rstrip("?")

    votes: dict[str, Counter] = defaultdict(Counter)
    ens: dict[str, Counter] = defaultdict(Counter)
    for path in glob.glob(str(LANG_DIR / "*" / "*.csv")):
        if args.baseline_git:
            import subprocess
            text = subprocess.run(["git", "show", f":{os.path.relpath(path, REPO)}"],
                                  capture_output=True, text=True, cwd=REPO).stdout
            import io
            fh = io.StringIO(text, newline="")
        else:
            fh = open(path, encoding="utf-8", newline="")
        with fh:
            for row in csv.reader(fh):
                if len(row) < 5 or not row[0].startswith("char-"):
                    continue
                cn, ru = row[1].strip(), row[4].strip()
                if not cn or not ru:
                    continue
                votes[cn][ru] += 1
                if row[3].strip() and not re.search(r"[\u3000-\u9fff]", row[3]):
                    ens[cn][row[3].strip()] += 1

    decisions: list[tuple[str, str, str, str, int, str]] = []
    for cn, counter in votes.items():
        if len(counter) < args.min_variants:
            continue
        en = ens[cn].most_common(1)[0][0] if ens[cn] else ""
        generic = is_generic(cn, en)

        if cn in registry:
            target = registry[cn]
            reason = "реестр"
        elif cn.isascii():
            lat = [(k, v) for k, v in counter.items() if k.isascii()]
            if lat:
                target = max(lat, key=lambda kv: kv[1])[0]
                reason = "CN латиницей — держим латиницу"
            else:
                continue
        elif re.fullmatch(r"[？?…]+", cn):
            target = "???"
            reason = "плейсхолдер"
        elif generic:
            # толпа: смысловые ключевые слова, потом частота
            scored = sorted(counter.items(), key=lambda kv: (-keyword_score(kv[0], en), -kv[1]))
            target = scored[0][0]
            reason = "ключевые слова + частота"
        else:
            # имя: транслитерация, но латинскую форму не навязываем
            scored = sorted(counter.items(), key=lambda kv: (-similarity(kv[0], en), -kv[1]))
            best = scored[0][0]
            best_sim = similarity(best, en)
            if best.lower() == (en or "").lower():
                cyr = [(k, v) for k, v in counter.items() if re.search(r"[\u0400-\u04ff]", k)]
                top_cyr = max(cyr, key=lambda kv: kv[1]) if cyr else None
                if top_cyr and top_cyr[1] >= counter[best]:
                    target, reason = top_cyr[0], f"латиница не навязываем (EN {en})"
                else:
                    target, reason = best, f"латиница как в EN ({en})"
            else:
                target, reason = best, f"близость к EN ({best_sim:.2f})"
        if target == counter.most_common(1)[0][0] and len(counter) == 1:
            continue
        rejected = ", ".join(f"{k}×{v}" for k, v in counter.most_common() if k != target)
        decisions.append((cn, en, target, rejected, sum(counter.values()), reason))

    decisions.sort(key=lambda d: (-d[4], d[0]))
    lines = [
        "# Сведение подписей говорящих к одной форме",
        "",
        "Отбор по английскому имени из игровых данных: личные имена — по транслитерации,",
        "обобщённые ярлыки — по ключевым словам EN, при равенстве — по частотности.",
        "",
        "| CN | EN | выбрано | отброшено | строк | почему |",
        "|---|---|---|---|---|---|",
    ]
    for cn, en, target, rejected, total, reason in decisions[: args.top]:
        lines.append(f"| {cn} | {en or '—'} | **{target}** | {rejected} | {total} | {reason} |")
    if len(decisions) > args.top:
        lines.append(f"\n… ещё {len(decisions) - args.top} (см. `--top`)")
    Path(args.md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"подписей с вариантами: {len(decisions)}")
    print(f"отчёт: {args.md}")
    for cn, en, target, rejected, total, reason in decisions[:12]:
        print(f"  {cn} [{en or '—'}] → {target}   ({reason}; было: {rejected[:50]})")

    if args.apply:
        # применяем именно вычисленные решения, а не реестр
        chosen = {cn: target for cn, _en, target, _rej, _n, _r in decisions}
        changed = 0
        import io

        for path in glob.glob(str(LANG_DIR / "*" / "*.csv")):
            text = Path(path).read_text(encoding="utf-8", newline="")
            eol = "\r\n" if "\r\n" in text else "\n"
            lines_in = text.splitlines(keepends=True)
            reader = csv.reader(lines_in)
            out: list[str] = []
            start = 0
            file_changed = False
            for row in reader:
                end = reader.line_num
                raw = "".join(lines_in[start:end])
                start = end
                if len(row) >= 5 and row[0].startswith("char-"):
                    target = chosen.get(row[1].strip())
                    if target and row[4] != target:
                        row[4] = target
                        buf = io.StringIO()
                        csv.writer(buf, lineterminator=eol).writerow(row)
                        out.append(buf.getvalue())
                        changed += 1
                        file_changed = True
                        continue
                out.append(raw)
            if file_changed:
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write("".join(out))
        print(f"\nприменено замен: {changed} (подписей затронуто: {len(chosen)})")
    else:
        print("\ndry-run (без записи)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())