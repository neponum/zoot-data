#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Досоздаёт CSV-шаблоны досье для оперативников без перевода.

Читалка подмешивает русский текст из `translation/ru_RU/dossiers/<id>.csv`
поверх официальной `handbook_info_table` (см. `ruCsvOverlayService`):
колонки `section_index`, `title_en`, `text_en`, `title_ru`, `text_ru`.
Пустые `title_ru`/`text_ru` означают «показывать английский» — поэтому шаблон
безопасно класть рядом с готовыми переводами.

Существующие файлы не трогаются.

    python3 tools/build_dossier_templates.py \
        --table ../.game-data/en/gamedata/excel/handbook_info_table.json
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "translation" / "ru_RU" / "dossiers"

COLUMNS = ["section_index", "title_en", "text_en", "title_ru", "text_ru"]


def section_text(entry: dict) -> str:
    stories = entry.get("stories") or []
    if not stories:
        return ""
    return (stories[0].get("storyText") or "").strip()


def main() -> None:
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    table = json.loads(args.table.read_text(encoding="utf-8"))
    handbook = table.get("handbookDict") or table
    args.out.mkdir(parents=True, exist_ok=True)

    created = 0
    for operator_id, entry in sorted(handbook.items()):
        target = args.out / f"{operator_id}.csv"
        if target.exists() or (args.out / f"{operator_id}.json").exists():
            continue
        rows = []
        for index, item in enumerate(entry.get("storyTextAudio") or []):
            title = (item.get("storyTitle") or "").strip()
            text = section_text(item)
            if not title and not text:
                continue
            rows.append([index, title, text, "", ""])
        if not rows:
            continue
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\r\n")
            writer.writerow(COLUMNS)
            writer.writerows(rows)
        created += 1

    print(f"новых шаблонов досье: {created}")


if __name__ == "__main__":
    main()
