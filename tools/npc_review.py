#!/usr/bin/env python3
"""Собирает список имён, переведённых по предположению (знак `?` в npc_labels.py).

Колонка EN берётся из игровых данных, чтобы сверять транслитерацию.

    python3 tools/npc_review.py [--md tools/npc_labels_review.md]
"""

from __future__ import annotations

import argparse
import csv
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from npc_labels import NPC_LABELS  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"


def collect_en() -> dict[str, str]:
    en: dict[str, str] = {}
    for path in glob.glob(str(LANG_DIR / "*" / "*.csv")):
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                if len(row) >= 5 and row[0].startswith("char-") and row[1].strip() and row[3].strip():
                    en.setdefault(row[1].strip(), row[3].strip())
    return en


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=str(REPO / "tools" / "npc_labels_review.md"))
    args = ap.parse_args()

    en = collect_en()
    rows = [(cn, ru[:-1], en.get(cn, "—")) for cn, ru in sorted(NPC_LABELS.items()) if ru.endswith("?")]

    out = [
        "# Имена, переведённые по предположению — нужна проверка NUM",
        "",
        "Источник: `tools/npc_labels.py` (знак `?` после перевода).",
        "Колонка EN — английское имя из игровых данных (пусто, если в игре его нет).",
        "Прошёл/не прошёл отмечай прямо здесь; снятые галочки переноси в `npc_labels.py`.",
        "",
        "| CN | EN | мой вариант | верно? |",
        "|---|---|---|---|",
    ]
    for cn, ru, e in rows:
        out.append(f"| {cn} | {e} | {ru} | ☐ |")

    Path(args.md).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{args.md}: {len(rows)} имён на проверку")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())