#!/usr/bin/env python3
"""Применяет точечные правки перевода из tools/patches/<эпизод>.py.

Каждая правка — тройка (файл, ID строки, было, стало). Если «было» не найдено
в текущем состоянии файла — правка считается конфликтом и не применяется,
патч завершается с ненулевым кодом. Пустой столбец `Character` означает
служебную строку (`__translator__` и т. п.), адресуемую по имени колонки.

    python3 tools/apply_patch.py a001             # dry-run
    python3 tools/apply_patch.py a001 --apply
"""

from __future__ import annotations

import argparse
import csv
import importlib
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG_DIR = REPO / "translation" / "ru_RU"
PATCHES_DIR = Path(__file__).resolve().parent / "patches"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("patch", help="имя патча без .py, например a001")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="показать каждую замену")
    args = ap.parse_args()

    mod = importlib.import_module(f"patches.{args.patch}")
    patches: list[tuple[str, str, str, str]] = mod.PATCHES

    by_file: dict[str, list[tuple[str, str, str]]] = {}
    for filename, row_id, old, new in patches:
        by_file.setdefault(filename, []).append((row_id, old, new))

    conflicts: list[str] = []
    applied = 0
    touched = 0

    for filename, items in sorted(by_file.items()):
        path = LANG_DIR / filename
        if not path.is_file():
            print(f"Нет файла: {path}", file=sys.stderr)
            return 2

        text = path.read_text(encoding="utf-8", newline="")
        eol = "\r\n" if "\r\n" in text else "\n"
        lines = text.splitlines(keepends=True)
        reader = csv.reader(lines)
        out: list[str] = []
        start = 0
        seen: set[str] = set()
        file_changed = False

        for row in reader:
            end = reader.line_num
            raw = "".join(lines[start:end])
            start = end

            new_row = list(row)
            if row:
                key = row[0] if row[0] else ""
                for row_id, old, new in items:
                    if row_id != key:
                        continue
                    # и служебные строки (__translator__,,Translator,,<ник>), и обычные
                    # хранят значение в пятой колонке
                    col = 4
                    if len(row) <= col:
                        conflicts.append(f"{filename} [{row_id}] — в строке нет пятой колонки")
                        continue
                    current = row[col]
                    if current == old:
                        new_row[col] = new
                    elif old in current:
                        # частичная правка: «было» — уникальный фрагмент поля
                        new_row[col] = current.replace(old, new)
                    elif new == current or (new in current and old not in current):
                        # правка уже применена ранее — считаем успехом
                        applied += 1
                        seen.add(row_id)
                        continue
                    else:
                        conflicts.append(
                            f"{filename} [{row_id}]\n     ожидалось: {old!r}\n     в файле:  {current!r}"
                        )
                        continue
                    applied += 1
                    seen.add(row_id)
                    file_changed = True
                    if args.verbose:
                        print(f"  {filename} {row_id}\n     было:  {old}\n     стало: {new}")

            if new_row != row:
                buf = io.StringIO()
                csv.writer(buf, lineterminator=eol).writerow(new_row)
                out.append(buf.getvalue())
            else:
                out.append(raw)

        missing = [rid for rid, _o, _n in items if rid not in seen]
        for rid in missing:
            if not any(c.startswith(filename) and f"[{rid}]" in c for c in conflicts):
                conflicts.append(f"{filename} [{rid}] — строка не найдена")

        if file_changed:
            touched += 1
            if args.apply and not any(c.startswith(filename) for c in conflicts):
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write("".join(out))

    print(f"\nправок в патче: {len(patches)}")
    print(f"применено: {applied}, файлов: {touched}")
    if conflicts:
        print(f"\nКОНФЛИКТЫ ({len(conflicts)}):")
        for c in conflicts:
            print("  -", c)
        print("\nПравки применены только в файлах без конфликтов.")
        return 1

    print("ПРИМЕНЕНО" if args.apply else "dry-run (без записи)")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(PATCHES_DIR.parent))
    raise SystemExit(main())