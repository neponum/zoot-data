# -*- coding: utf-8 -*-
"""Проход по именам собственным: приведение прозы к канону подписей.

Таблица берётся из подписей char-N (они уже сверены с английским Reference) и
из глоссария сайта. Меняется только колонка Translation (5-я) — в ней лежат
и подписи char-N, и весь текст.

Запуск: python3 tools/apply_names.py [--apply] [--only хосигума]
"""
import csv
import glob
import re
import sys
from collections import Counter

APPLY = "--apply" in sys.argv

# (неверно, верно) — верно подтверждено подписями char-N и src/data/operator_names_map.json
FIXES = [
    # 星熊 Hoshiguma: подписи и сайт дают «Хошигума», в прозе была опечатка «Хосигума»
    ("хосигума", "хошигума"),
    ("хосигумы", "хошигумы"),
    ("хосигуму", "хошигуму"),
    ("хосигуме", "хошигуме"),
    ("хосигумой", "хошигумой"),
    # 企鹅物流 Penguin Logistics: канон пользователя — «Пингвин Лоджистикс»
    (r"Пингвин\s+Логистикс?", "Пингвин Лоджистикс"),
    (r"Пингвин Лоджистик(?!с)", "Пингвин Лоджистикс"),
]

ONLY = None
if "--only" in sys.argv:
    ONLY = sys.argv[sys.argv.index("--only") + 1]
    FIXES = [f for f in FIXES if ONLY in f[0]]

stats = Counter()
changed_files = 0
changed_rows = 0


def convert(cell):
    for wrong, right in FIXES:
        if wrong.startswith("Пингвин"):
            cell = re.sub(wrong, right, cell, flags=re.IGNORECASE)
            continue
        cell = re.sub(r"(?<![А-Яа-яЁё])" + wrong + r"(?![А-Яа-яЁё])", right, cell)
        cell = re.sub(
            r"(?<![А-Яа-яЁё])" + wrong.capitalize() + r"(?![А-Яа-яЁё])",
            right.capitalize(),
            cell,
        )
    return cell


for path in sorted(glob.glob("translation/ru_RU/*/*.csv")):
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    newline = "\r\n" if "\r\n" in raw else "\n"
    rows = list(csv.reader(raw.splitlines(keepends=True)))
    dirty = False

    for row in rows:
        if len(row) < 5:
            continue
        new = convert(row[4])
        if new != row[4]:
            stats[row[4].strip()[:34]] += 1
            row[4] = new
            dirty = True

    if dirty:
        changed_files += 1
        changed_rows += 1
        if APPLY:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                csv.writer(fh, lineterminator=newline).writerows(rows)

print("режим:", "ПРИМЕНЕНИЕ" if APPLY else "пробный (--apply не указан)")
print("правил в таблице:", len(FIXES))
print("строк изменено:", changed_rows, "| файлов:", changed_files, "| ячеек:", sum(stats.values()))
for cell, n in stats.most_common(12):
    print(f"   {n:3}  {cell}")
