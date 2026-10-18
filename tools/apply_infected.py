# -*- coding: utf-8 -*-
"""Единый проход: «заражённый» → «инфицированный» по всем переводам ru_RU.

Канон пользователя: Infected → Инфицированные (везде, включая прозу).
Меняются только причастия и прилагательные — то есть носители признака:
заражённый, заражённых, заражена и т.п. Глаголы и существительные процесса
(заразиться, заражение, заражения, заражается, заражают, заражусь) НЕ трогаются:
это про заражение, а не про инфицированных. «Незаражённые» тоже не трогаются:
там «не-» часть слова.

Запуск: python3 tools/apply_infected.py [--apply]
"""
import csv
import glob
import re
import sys
from collections import Counter

APPLY = "--apply" in sys.argv

STEMS = ["зараженн", "заражённ", "зараженна", "заражённа", "заражен", "заражён"]
FORMS = [
    "зараженными", "зараженными", "зараженного", "зараженному", "зараженным",
    "зараженную", "зараженной", "зараженные", "зараженный", "зараженная",
    "зараженное", "зараженных", "заражены", "заражена", "заражено", "заражен",
    "зараженна",
    "заражёнными", "заражённого", "заражённому", "заражённым", "заражённую",
    "заражённой", "заражённые", "заражённый", "заражённая", "заражённое",
    "заражённых", "заражёны", "заражёна", "заражёно", "заражён",
]


def target(form):
    for stem in sorted(STEMS, key=len, reverse=True):
        if form.startswith(stem):
            return "инфицирован" + form[len(stem):]
    raise ValueError(form)


TABLE = sorted(((f, target(f)) for f in FORMS), key=lambda p: -len(p[0]))
# Опечатки в самом термине (одиночная «н»): однозначные формы
SPELLING = [
    "инфицироваными", "инфицированых", "инфицированые", "инфицированым",
    "инфицированый", "инфицированого", "инфицированому", "инфицированой",
    "инфицированое",
    # обрыв формы: «вы ведь инфицированя» → «инфицированная»
    "инфицированя", "Инфицированя",
]
SPELLING += [w.capitalize() for w in SPELLING]

RE_REMAIN = re.compile(r"[Зз]ара[ж][а-яё]+")


def convert(cell):
    for src in SPELLING:
        cell = re.sub(r"(?<![А-Яа-яЁё])" + src + r"(?![А-Яа-яЁё])",
                      src.replace("инфицирова", "инфицирован").replace("Инфицирова", "Инфицирован"), cell)
    for src, dst in TABLE:
        cell = re.sub(r"(?<![А-Яа-яЁё])" + src + r"(?![А-Яа-яЁё])", dst, cell)
        cell = re.sub(
            r"(?<![А-Яа-яЁё])" + src.capitalize() + r"(?![А-Яа-яЁё])",
            dst.capitalize(),
            cell,
        )
    return cell


changed_files = 0
changed_rows = 0
leftovers = Counter()
examples = []

for path in sorted(glob.glob("translation/ru_RU/*/*.csv")):
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    newline = "\r\n" if "\r\n" in raw else "\n"
    rows = list(csv.reader(raw.splitlines(keepends=True)))
    dirty = False

    for row in rows:
        for idx in (0, 4):
            if idx >= len(row):
                continue
            if idx == 0 and not row[0].startswith("char-"):
                continue
            new = convert(row[idx])
            if new != row[idx]:
                row[idx] = new
                dirty = True
        if len(row) > 4:
            found = RE_REMAIN.findall(row[4])
            if found:
                leftovers.update(m.lower() for m in found)
                examples.append((path, row[0], found, row[4][:70]))

    if dirty:
        changed_files += 1
        changed_rows += 1
        if APPLY:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                csv.writer(fh, lineterminator=newline).writerows(rows)

print("режим:", "ПРИМЕНЕНИЕ" if APPLY else "пробный (--apply не указан)")
print("строк изменено:", changed_rows, "| файлов:", changed_files)
print("\nостатки «зараж-» после прохода:")
for form, count in leftovers.most_common():
    print(f"   {form:>14} {count}")
print("строк с остатками:", len(examples))
