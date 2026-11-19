#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Досоздаёт CSV-шаблоны эпизодов, у которых ещё нет файла перевода.

Читалка ищет перевод как `translation/<lang>/<эпизод>/<сценарий>[_<ник>].csv`,
поэтому шаблон — обычный файл без суффикса: переводчик заполняет колонку
`Translation`, и он сразу становится переводом.

Скрипт идемпотентен: существующие файлы (в том числе чужие переводы) не
трогаются, добавляются только отсутствующие сценарии.

Запуск (в CI — `.github/workflows/sync-content.yml`):

    python3 tools/build_episode_templates.py \
        --stories ../.game-data/cn/gamedata/story \
        --titles ../.game-data/cn/gamedata/excel/story_review_table.json
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "translation" / "ru_RU"

TAG_PREFIX = re.compile(
    r"^(\s*(?:\[(?:[^\"'\]]|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')*\]\s*)*)(.*)$"
)
NAME = re.compile(r'name="([^"]+)"')
INNER_TEXT = (
    re.compile(r'\[Subtitle[^\]]*text="([^"]+)"', re.IGNORECASE),
    re.compile(r'\[Sticker[^\]]*text="([^"]+)"', re.IGNORECASE),
    re.compile(r'options="([^"]+)"', re.IGNORECASE),
)


def parse_lines(raw: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, line in enumerate(raw.split("\n")):
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("//") or trimmed.upper().startswith("[HEADER"):
            continue
        match = TAG_PREFIX.match(line)
        prefix, text = (match.group(1), match.group(2)) if match else ("", line)
        if re.search(r"\[delay\b", prefix, re.IGNORECASE):
            continue
        text = text.strip()
        if not text:
            for pattern in INNER_TEXT:
                inner = pattern.search(prefix)
                if inner:
                    text = inner.group(1)
                    break
        if not text:
            continue
        name = NAME.search(line)
        rows.append({"id": f"line-{index}", "name": name.group(1) if name else "", "text": text})
    return rows


def build_csv(source: str, chapter: str, episode: str, title: str) -> str:
    lines = parse_lines(source)
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(["ID", "Character", "Original Text", "Reference", "Translation"])
    writer.writerow(["__translator__", "", "Translator", "", "tbd"])
    writer.writerow(["__language__", "", "Language", "en_US", "ru_RU"])
    writer.writerow(["__episode__", "", "Episode ID", "", chapter])
    writer.writerow(["__chapter__", "", "Chapter Name", f"{chapter}/{episode}", title])
    writer.writerow(["", "", "", "", ""])

    seen: dict[str, int] = {}
    for row in lines:
        if row["name"] and row["name"] not in seen:
            seen[row["name"]] = len(seen) + 1
    for name, number in seen.items():
        writer.writerow([f"char-{number}", name, name, "", ""])
    if seen:
        writer.writerow(["", "", "", "", ""])

    for row in lines:
        writer.writerow([row["id"], row["name"], row["text"], "", ""])
    return buffer.getvalue()


def episode_folder(base: str) -> str:
    """`level_act55side_st01` → `act55side` (как getEpisodeFolderForStory)."""
    if base.startswith("level_"):
        return base[len("level_"):].split("_", 1)[0]
    return "misc"


def load_titles(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    table = json.loads(path.read_text(encoding="utf-8"))
    titles: dict[str, str] = {}
    for key, entry in table.items():
        for info in entry.get("infoUnlockDatas") or []:
            story = info.get("storyTxt")
            if story:
                titles[story] = info.get("storyName") or entry.get("name") or ""
    return titles


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stories", required=True, type=Path)
    parser.add_argument("--titles", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    titles = load_titles(args.titles)
    bases = {path.stem for path in args.out.glob("**/*.csv")}
    created = 0

    for path in sorted(args.stories.glob("**/level_*.txt")):
        base = path.stem
        if any(name == base or name.startswith(base + "_") for name in bases):
            continue
        relative = path.relative_to(args.stories).with_suffix("").as_posix()
        folder = episode_folder(base)
        payload = build_csv(
            path.read_text(encoding="utf-8"),
            f"activities/{folder}" if folder != "main" else "obt/main",
            base,
            titles.get(relative, ""),
        )
        target = args.out / folder / f"{base}.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8", newline="")
        bases.add(base)
        created += 1

    print(f"новых шаблонов эпизодов: {created}")


if __name__ == "__main__":
    main()
