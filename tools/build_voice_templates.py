#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Досоздаёт CSV-шаблоны реплик оперативников.

Читалка берёт реплики из официальной `charword_table` и подмешивает русский
текст из `translation/ru_RU/voices/<operator_id>.csv` (см.
`ruCsvOverlayService`). Колонки: `id`, `title`, `original` (EN),
`original_zh` (ZH), `translation` (RU). Основой для перевода служит
китайский текст; английский — только подсказка. Пустая `translation` =
показывать оригинал.

Существующие файлы не трогаются.

    python3 tools/build_voice_templates.py \
        --table ../.game-data/en/gamedata/excel/charword_table.json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "translation" / "ru_RU" / "voices"

COLUMNS = ["id", "title", "original", "original_zh", "translation"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, type=Path)
    parser.add_argument("--zh-table", type=Path, help="китайская charword_table для колонки original_zh")
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    table = json.loads(args.table.read_text(encoding="utf-8"))
    words = table.get("charWords") or {}
    zh_words = {}
    if args.zh_table:
        zh_words = (json.loads(args.zh_table.read_text(encoding="utf-8")).get("charWords") or {})
    args.out.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in words.values():
        char_id = entry.get("charId") or entry.get("wordKey") or ""
        if not char_id:
            continue
        grouped[char_id].append(entry)

    created = 0
    for operator_id, lines in sorted(grouped.items()):
        target = args.out / f"{operator_id}.csv"
        if target.exists():
            continue
        lines.sort(key=lambda item: int(item.get("voiceIndex") or 0))
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\r\n")
            writer.writerow(COLUMNS)
            for line in lines:
                writer.writerow(
                    [
                        line.get("charWordId") or "",
                        line.get("voiceTitle") or "",
                        (line.get("voiceText") or "").replace("\n", "\\n"),
                        (zh_words.get(line.get("charWordId"), {}).get("voiceText") or "").replace("\n", "\\n"),
                        "",
                    ]
                )
        created += 1

    print(f"новых шаблонов реплик: {created}")


if __name__ == "__main__":
    main()
