#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Обновляет `translation/ru_RU/episodes.json` — снимок структуры переводов.

Для каждого эпизода считает файлы, переводчиков и карту `scenes`
(`<сценарий> → <ник>`). Переводчик определяется по имени:
`<сценарий>_<ник>.csv`, где `<сценарий>` — реальное базовое имя из игровых
данных (`--stories`), а файл без суффикса — общий перевод. Карта `scenes`
позволяет сайту открыть точный файл одним запросом, не перебирая авторов.

    python3 tools/build_index.py --stories ../.game-data/cn/gamedata/story
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORY_DIR = ROOT / "translation" / "ru_RU" / "story"
INDEX_PATH = ROOT / "translation" / "ru_RU" / "episodes.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stories", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=INDEX_PATH)
    args = parser.parse_args()

    # Берём все сценарии, а не только level_*: в папках ui/guide/story тоже
    # лежат файлы с суффиксом автора.
    bases = {path.stem for path in args.stories.rglob("*.txt")}
    bases_by_length = sorted(bases, key=len, reverse=True)
    index: dict[str, dict[str, object]] = {}

    for folder in sorted(p for p in STORY_DIR.iterdir() if p.is_dir()):
        files = sorted(folder.glob("*.csv"))
        if not files:
            continue
        scenes: dict[str, str] = {}
        for path in files:
            stem = path.stem
            if stem in bases:
                scenes[stem] = ""
                continue
            match = next(
                (base for base in bases_by_length if stem.startswith(base + "_")),
                None,
            )
            if match:
                scenes[match] = stem[len(match) + 1:]
            else:
                # Игрового имени нет под рукой — считаем файл общим.
                scenes[stem] = ""
        index[folder.name] = {
            "files": len(files),
            "translators": sorted({t for t in scenes.values() if t}),
            "scenes": scenes,
        }

    args.out.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"эпизодов в индексе: {len(index)}")


if __name__ == "__main__":
    main()
