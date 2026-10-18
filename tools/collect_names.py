#!/usr/bin/env python3
"""Собирает реестр имён говорящих (строки char-N) из CSV-переводов.

Показывает, как один и тот же персонаж подписан по-разному, и находит
явно битые подписи: непереведённые (китайские), служебные ID ассетов,
латиница вместо кириллицы, кавычки внутри тега.

    python3 tools/collect_names.py                 # отчёт в stdout
    python3 tools/collect_names.py --md names.md   # отчёт в файл
    python3 tools/collect_names.py --top 40
"""

from __future__ import annotations

import argparse
import csv
import glob
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"

CJK_RE = re.compile(r"[\u3000-\u9fff\uff00-\uffef]")
ASSET_ID_RE = re.compile(r"(avg_|char_\d|npc_|char_[a-z])", re.I)
LATIN_RE = re.compile(r"[A-Za-z]")
CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")


def label_class(ru: str) -> str | None:
    if CJK_RE.search(ru):
        return "не переведено"
    if ASSET_ID_RE.search(ru):
        return "ID ассета"
    if not CYRILLIC_RE.search(ru) and LATIN_RE.search(ru):
        return "латиница"
    if ru.count("«") or ru.count("\"") or ru.count("“"):
        return "кавычки в теге"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", help="записать отчёт в этот файл")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--episode", help="ограничить одним эпизодом")
    args = ap.parse_args()

    files = sorted(glob.glob(str(LANG_DIR / (args.episode or "*") / "*.csv")))

    # cn -> ru -> счётчик(эпизод, файл); en используется для сверки перевода
    by_cn: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    by_ru: dict[str, set] = defaultdict(set)
    by_cn_en: dict[str, set] = defaultdict(set)
    ru_to_en: dict[str, set] = defaultdict(set)

    for path in files:
        ep = Path(path).parent.name
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                if len(row) < 5 or not row[0].startswith("char-"):
                    continue
                cn, ru = row[1].strip(), row[4].strip()
                if not cn or not ru:
                    continue
                by_cn[cn][ru].add(ep)
                by_ru[ru].add(cn)
                if row[3].strip():
                    by_cn_en[cn].add(row[3].strip())
                    ru_to_en[ru].add(row[3].strip())

    lines: list[str] = []
    multi = {cn: rus for cn, rus in by_cn.items() if len(rus) > 1}
    broken = [
        (cn, ru, cls)
        for cn, rus in by_cn.items()
        for ru, _eps in rus.items()
        if (cls := label_class(ru))
    ]

    lines.append("# Реестр имён говорящих (char-N)\n")
    lines.append(f"- Персонажей всего (уникальных CN-подписей): **{len(by_cn)}**")
    lines.append(f"- Персонажей с >1 вариантом RU-подписи: **{len(multi)}**")
    lines.append(f"- Битые подписи (не переведено / ID ассета / кавычки): **{len(broken)}**\n")

    lines.append("\n## Битые подписи\n")
    lines.append("| CN | EN | RU | проблема |")
    lines.append("|---|---|---|---|")
    for cn, ru, cls in sorted(broken, key=lambda x: x[2])[:120]:
        en = ", ".join(sorted(by_cn_en.get(cn, []))) or "—"
        lines.append(f"| {cn} | {en} | {ru} | {cls} |")

    lines.append("\n\n## Топ персонажей по числу вариантов\n")
    lines.append("Колонка EN — английское имя из игровых данных, чтобы сверять перевод.\n")
    lines.append("| CN | EN | вариантов | варианты RU |")
    lines.append("|---|---|---|---|")
    for cn, rus in sorted(multi.items(), key=lambda kv: -len(kv[1]))[: args.top]:
        en = ", ".join(sorted(by_cn_en.get(cn, []))) or "—"
        lines.append(f"| {cn} | {en} | {len(rus)} | {', '.join(sorted(rus))} |")

    # русская подпись, у которой в игре несколько английских имён
    variants_conflicting = [ru for ru in by_ru if len(ru_to_en.get(ru, set())) > 1]

    lines.append("\n\n## Сверка: русская подпись → английские оригиналы (где английских имён несколько)\n")
    lines.append("Такие подписи почти всегда означают склейку разных персонажей.\n")
    lines.append("| RU | EN |")
    lines.append("|---|---|")
    for ru in sorted(variants_conflicting)[: args.top]:
        ens = sorted(ru_to_en.get(ru, []))
        lines.append(f"| {ru} | {', '.join(ens)} |")

    report = "\n".join(lines) + "\n"

    if args.md:
        out = Path(args.md) if Path(args.md).is_absolute() else REPO / args.md
        out.write_text(report, encoding="utf-8")
        print(f"отчёт: {out}")
        print(f"персонажей: {len(by_cn)}, с вариантами: {len(multi)}, битых: {len(broken)}")
    else:
        print(report[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())