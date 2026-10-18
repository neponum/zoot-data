# -*- coding: utf-8 -*-
"""Проход по канону, утверждённому пользователем (5 решений).

1. 术师 Caster → «кастер» (в подписях и прозе), прилагательные и «маги» не трогаем
2. 源石技艺 Arts → «Искусство» (ед. ч.), во всех падежах
3. 罗德岛 Rhodes Island → «Родос» (без «Айленд»), с пересчётом падежей
4. ё: слова из закрытого списка, где «е» — ошибка
5. Тире подряд (——, ———…) → одинарное «—»

Запуск: python3 tools/apply_canon.py [--apply] [--only родос|кастер|искусство|ё|тире]
"""
import csv
import glob
import re
import sys
from collections import Counter

APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

# --- 1. кастер -------------------------------------------------------------------------
CASTER = [
    ("заклинательниц", "кастериц"),
    ("заклинатели", "кастеры"),
    ("заклинателей", "кастеров"),
    ("заклинателем", "кастером"),
    ("заклинателю", "кастеру"),
    ("заклинателя", "кастера"),
    ("заклинатель", "кастер"),
]

# --- 2. Искусство ----------------------------------------------------------------------
ARTS = [
    ("Искусствами", "Искусством"),
    ("Искусствам", "Искусству"),
    ("Искусствах", "Искусстве"),
    ("Искусства", "Искусство"),
]

# --- 3. Родос --------------------------------------------------------------------------
RHODES = [
    (r"Родос-Айлендом", "Родосом"),
    (r"Родос-Айленду", "Родосу"),
    (r"Родос-Айленде", "Родосе"),
    (r"Родос-Айленда", "Родоса"),
    (r"Родос-Айленд", "Родос"),
    (r"Родос Айлендом", "Родосом"),
    (r"Родос Айленду", "Родосу"),
    (r"Родос Айленде", "Родосе"),
    (r"Родос Айленда", "Родоса"),
    (r"Родос Айленд", "Родос"),
]

# --- 4. ё: см. отдельный инструмент tools/apply_yo.py ---------------------------

# --- 5. тире ---------------------------------------------------------------------------
DASHES = re.compile(r"—{2,}")

RULES = {"кастер": CASTER, "искусство": ARTS, "родос": RHODES}
ORDER = ["кастер", "искусство", "родос"]


def convert_caster(cell):
    for wrong, right in CASTER:
        cell = re.sub(r"(?<![А-Яа-яЁё])" + wrong, right, cell)
        cell = re.sub(r"(?<![А-Яа-яЁё])" + wrong.capitalize(), right.capitalize(), cell)
    return cell


def convert_arts(cell):
    for wrong, right in ARTS:
        cell = re.sub(r"(?<![А-Яа-яЁё])" + wrong + r"(?![А-Яа-яЁё])", right, cell)
    return cell


def convert_rhodes(cell):
    for wrong, right in RHODES:
        cell = re.sub(wrong, right, cell)
    return cell


def convert_yo(cell):
    raise SystemExit("проход «ё» живёт в tools/apply_yo.py: список слов там проверенный")


def convert_dashes(cell):
    return DASHES.sub("—", cell)


CONVERTERS = {
    "кастер": convert_caster,
    "искусство": convert_arts,
    "родос": convert_rhodes,
    "ё": convert_yo,
    "тире": convert_dashes,
}
active = [k for k in ORDER if ONLY is None or k == ONLY]
if ONLY in ("ё", "тире"):
    active.append(ONLY)

stats = Counter()
changed_files = 0
changed_rows = 0
risky = []

for path in sorted(glob.glob("translation/ru_RU/*/*.csv")):
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    newline = "\r\n" if "\r\n" in raw else "\n"
    rows = list(csv.reader(raw.splitlines(keepends=True)))
    dirty = False

    for row in rows:
        if len(row) < 5:
            continue
        before = row[4]
        cell = before
        for key in active:
            cell = CONVERTERS[key](cell)
        if cell != before:
            row[4] = cell
            dirty = True
            changed_rows += 1
            for key in active:
                if CONVERTERS[key](before) != before:
                    stats[key] += 1
            # согласие после перевода «Искусства» → «Искусство»
            if "Искусство" in cell and re.search(
                r"\b(какие|каких|которые|эти|те|лечебные|мерзкие|проклятые|различные|"
                r"другие|свои|чужие|мощные|разрушительные|прочие|все|всех)\s+Искусство\b",
                cell,
            ):
                risky.append((path.split("/")[-1], row[0], cell[:120]))

    if dirty:
        changed_files += 1
        if APPLY:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                csv.writer(fh, lineterminator=newline).writerows(rows)

print("режим:", "ПРИМЕНЕНИЕ" if APPLY else "пробный (--apply не указан)")
print("активные правила:", active)
print("строк изменено:", changed_rows, "| файлов:", changed_files)
print("по правилам:", dict(stats))
print("\nстроки, где после перехода на «Искусство» нужно поправить согласие:", len(risky))
for item in risky[:25]:
    print("  ", item[0][:30], item[1], "|", item[2])
