#!/usr/bin/env python3
"""Находит дубли: ИИ-перевод (nep0num) рядом с переводом человека.

Имя файла: <storyBaseName>_<translator>.csv, папка = эпизод.
Если на одну главу есть и `nep0num`, и перевод живого переводчика —
оставляем только перевод человека, ИИ-дубликат удаляем.

    python3 tools/dedupe_translations.py            # отчёт, ничего не удаляет
    python3 tools/dedupe_translations.py --apply    # удалить через git rm
    python3 tools/dedupe_translations.py --episode a001
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"

AI_TRANSLATORS = {"nep0num", "neponum"}
KNOWN = sorted(
    AI_TRANSLATORS
    | {
        "neksi0762", "frostymisery17", "naoshka_v", "ilarhion", "num4ar",
        "vendigo", "myshanin", "centurion_vendigo",
    },
    key=len, reverse=True,
)


def split_name(path: Path) -> tuple[str, str]:
    """Отрезает суффикс переводчика. Список отсортирован по длине, поэтому
    `centurion_vendigo` побеждает `vendigo`."""
    stem = path.stem
    m = re.search(r"_(" + "|".join(re.escape(k) for k in KNOWN) + r")$", stem)
    return (stem[: m.start()], m.group(1)) if m else (stem, "?")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="удалить ИИ-дубликаты (git rm)")
    ap.add_argument("--episode", help="ограничить одной папкой эпизода")
    args = ap.parse_args()

    groups: dict[tuple[str, str], list[tuple[Path, str]]] = defaultdict(list)
    dirs = [LANG_DIR / args.episode] if args.episode else sorted(p for p in LANG_DIR.iterdir() if p.is_dir())
    for d in dirs:
        if not d.is_dir():
            print(f"Нет папки: {d}")
            return 2
        for f in sorted(d.glob("*.csv")):
            base, tr = split_name(f)
            groups[(d.name, base)].append((f, tr))

    to_delete: list[Path] = []
    rows: list[str] = []
    for (ep, base), files in sorted(groups.items()):
        ai = [(f, tr) for f, tr in files if tr in AI_TRANSLATORS]
        humans = [(f, tr) for f, tr in files if tr not in AI_TRANSLATORS]
        if ai and humans:
            for f, tr in ai:
                to_delete.append(f)
                rows.append(f"{ep}/{base}: оставить {sorted(t for _f, t in humans)}, удалить {tr}")

    ai_only = sum(1 for files in groups.values() if files and all(tr in AI_TRANSLATORS for _f, tr in files))
    humans_total = sum(len([1 for _f, tr in files if tr not in AI_TRANSLATORS]) for files in groups.values())

    print(f"глав всего: {len(groups)}")
    print(f"переводов человека: {humans_total}")
    print(f"глав, где перевод только ИИ: {ai_only}")
    print(f"глав с дублем ИИ + человек: {len(rows)}\n")
    for r in rows:
        print("  " + r)

    if not to_delete:
        print("\nдублей нет")
        return 0

    if args.apply:
        import subprocess

        rels = [str(p.relative_to(REPO)) for p in to_delete]
        # -f: в индексе лежат наши же правки (переезды и термины), удаляем принудительно
        subprocess.run(["git", "rm", "-f", "--", *rels], cwd=REPO, check=True)
        print(f"\nУДАЛЕНО файлов: {len(rels)}")
    else:
        print(f"\ndry-run: к удалению {len(to_delete)} файлов (ничего не изменено)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())