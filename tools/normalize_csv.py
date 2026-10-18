#!/usr/bin/env python3
"""Нормализация CSV-переводов Zoot Data.

Правит ТОЛЬКО колонку Translation (5-ю) и служебные строки не трогает.
Оригинальный китайский текст и английский референс остаются байт-в-байт.

Использование:
    python3 tools/normalize_csv.py <эпизод> [...]        # dry-run по умолчанию
    python3 tools/normalize_csv.py <эпизод> [...] --apply
    python3 tools/normalize_csv.py all --apply
    python3 tools/normalize_csv.py a001 --rules invisible,spaces,punct --apply
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"

ALL_RULES = ("invisible", "spaces", "punct")

INVISIBLE_RE = re.compile("[\u200b\u200c\u200d\ufeff\u00ad]")
MULTISPACE_RE = re.compile(r"[ \t\u00a0]{2,}")
# «а,, б» → «а, б»: запятая идёт вместо второй запятой, пробел после неё сохраняется
DOUBLE_COMMA_RE = re.compile(r",\s*(?=[,?!:.])")
# «Рык»и крик → «Рык» и крик: после закрывающей лапки перед словом нужен пробел
CLOSE_QUOTE_GLUE_RE = re.compile(r"\u00bb(?=[\u0410-\u042f\u0430-\u044fA-Za-z])")
# артефакт машины: «Мама!..» и «поможет?..» — две точки после знака вместо многоточия
DOUBLE_DOT_TAIL_RE = re.compile(r"([!?])\.\.(?=[\s\u00bb\u201d\"')]|$)")
# машинный артефакт: «поздно--» вместо тире
DOUBLE_HYPHEN_RE = re.compile(r"--(?=[\s\u00bb\u201d\"')]|$)")
SPACED_HYPHEN_RE = re.compile(r"(?<=\s)-(?=\s)")
SPACED_ENDASH_RE = re.compile(r"(?<=\s)\u2013(?=\s)")
LONG_ELLIPSIS_RE = re.compile(r"\.{3,}")  # 4+ точек → ровно три (канон: «...»)
# символ «…» в переводах не используем — канон три точки
CHAR_ELLIPSIS_RE = re.compile("\u2026+")
ELLIPSIS_RE = re.compile(r"(?<!\.)\.{3}(?!\.)")


def clean(value: str, rules: tuple[str, ...], opts: dict) -> tuple[str, list[str]]:
    """Возвращает (исправленное_значение, список_применённых_правил)."""
    original = value
    applied: list[str] = []

    if "invisible" in rules:
        fixed = INVISIBLE_RE.sub("", value).replace("\u00a0", " ")
        if fixed != value:
            applied.append("invisible")
            value = fixed

    if "spaces" in rules:
        fixed = MULTISPACE_RE.sub(" ", value).strip()
        if fixed != value:
            applied.append("spaces")
            value = fixed

    if "punct" in rules:
        fixed = value
        if not opts.get("keep_hyphen", False):
            fixed = SPACED_ENDASH_RE.sub("—", fixed)
            fixed = SPACED_HYPHEN_RE.sub("—", fixed)
        fixed = CLOSE_QUOTE_GLUE_RE.sub("» ", fixed)      # «Рык»и крик → «Рык» и крик
        fixed = DOUBLE_DOT_TAIL_RE.sub("\\1...", fixed)    # Мама!.. → Мама!...
        fixed = DOUBLE_HYPHEN_RE.sub("—", fixed)           # поздно-- → поздно—
        if opts.get("fix_double_comma", True):
            fixed = DOUBLE_COMMA_RE.sub(",", fixed)
        if opts.get("ellipsis_char", False):
            fixed = ELLIPSIS_RE.sub("…", fixed)
        fixed = CHAR_ELLIPSIS_RE.sub("...", fixed)        # «……» → «...»
        fixed = LONG_ELLIPSIS_RE.sub("...", fixed)         # 4+ точек → ровно три
        if fixed != value:
            applied.append("punct")
            value = fixed

    return (value, applied) if value != original else (original, [])


def iter_rows_with_raw(text: str):
    """Отдаёт (логическая_строка, сырой_текст) — сырой текст копируется байт-в-байт."""
    lines = text.splitlines(keepends=True)
    reader = csv.reader(lines)
    start = 0
    for row in reader:
        end = reader.line_num
        yield row, "".join(lines[start:end])
        start = end


def process(path: Path, rules: tuple[str, ...], opts: dict, apply: bool) -> tuple[int, list[tuple[int, str, str]]]:
    # newline="" — иначе Python нормализует CRLF в LF и весь файл уходит в дифф
    text = path.read_text(encoding="utf-8", newline="")
    eol = "\r\n" if "\r\n" in text else "\n"
    out: list[str] = []
    changes: list[tuple[int, str, str]] = []
    changed_rows = 0

    for n, (row, raw) in enumerate(iter_rows_with_raw(text), 1):
        if len(row) < 5 or not row[0] or row[0].startswith("__"):
            out.append(raw)
            continue
        fixed, applied = clean(row[4], rules, opts)
        if not applied:
            out.append(raw)
            continue
        row[4] = fixed
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator=eol)
        writer.writerow(row)
        out.append(buf.getvalue())
        changed_rows += 1
        changes.append((n, row[0], f"{fixed[:78]}"))

    if changed_rows and apply:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(out))

    return changed_rows, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="папка эпизода (main, a001, …) или all")
    ap.add_argument("--apply", action="store_true", help="записать изменения (по умолчанию dry-run)")
    ap.add_argument("--rules", default=",".join(ALL_RULES), help=f"правила через запятую: {ALL_RULES} + punct")
    ap.add_argument("--ellipsis-char", action="store_true", help="многоточия → символ «…»")
    ap.add_argument("--keep-hyphen", action="store_true", help="не менять « - » на « — »")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rules = tuple(r.strip() for r in args.rules.split(",") if r.strip())
    unknown = set(rules) - set(ALL_RULES)
    if unknown:
        print(f"Неизвестные правила: {unknown}", file=sys.stderr)
        return 2

    dirs = (
        sorted(p for p in LANG_DIR.iterdir() if p.is_dir())
        if "all" in args.targets
        else [LANG_DIR / t for t in args.targets]
    )

    opts = {
        "ellipsis_char": args.ellipsis_char,
        "keep_hyphen": args.keep_hyphen,
    }

    total_rows = 0
    total_files = 0
    for d in dirs:
        if not d.is_dir():
            print(f"Нет такой папки: {d}", file=sys.stderr)
            return 2
        for f in sorted(d.glob("*.csv")):
            count, changes = process(f, rules, opts, args.apply)
            if count:
                total_files += 1
                total_rows += count
                if not args.quiet:
                    print(f"\n{f.relative_to(REPO)} — {count} строк")
                    for n, rid, sample in changes:
                        print(f"   строка {n:>4} {rid:<8} {sample}")

    mode = "ПРИМЕНЕНО" if args.apply else "dry-run"
    print(f"\n{mode}: файлов {total_files}, строк {total_rows}, правила {rules}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())