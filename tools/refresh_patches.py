# -*- coding: utf-8 -*-
"""Пересобирает «было» в патчах после глобальных проходов по канону.

Глобальные проходы (инфицированные, Хошигума, Пингвин Лоджистикс, кастер,
Искусство, Родос, тире, ё) меняют текст тех же строк, которые лежат в патчах
глав. Для каждой правки:

  * если в файле уже стоит «стало» — правка сделана, кортеж удаляется;
  * если в файле стоит «было» — всё как было, кортеж остаётся;
  * если текст отличается только результатом проходов — «было» пересобирается;
  * иначе правка попадает в отчёт как ручной конфликт.

Запуск: python3 tools/refresh_patches.py main_03_* main_04_*
"""
import csv
import glob
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)


def load_transforms():
    canon_ns = {}
    src = open(os.path.join(HERE, "apply_canon.py"), encoding="utf-8").read()
    exec(src.split("RULES = {")[0].replace("sys.argv", "[]"), canon_ns)
    funcs = src.split("def convert_caster")[1].split("CONVERTERS")[0]
    exec("def convert_caster" + funcs, canon_ns)
    yo_ns = {}
    src = open(os.path.join(HERE, "apply_yo.py"), encoding="utf-8").read()
    exec(src.split("stats = Counter()")[0].replace("sys.argv", "[]"), yo_ns)

    def transform(cell):
        cell = canon_ns["convert_caster"](cell)
        cell = canon_ns["convert_arts"](cell)
        cell = canon_ns["convert_rhodes"](cell)
        cell = canon_ns["convert_dashes"](cell)
        for wrong, right in yo_ns["PAIRS"]:
            for w, r in ((wrong, right), (wrong.capitalize(), right.capitalize())):
                cell = re.sub(r"(?<![А-Яа-яЁё])" + re.escape(w) + r"(?![А-Яа-яЁё])", r, cell)
        return cell

    return transform


def read_rows(rel):
    with open(os.path.join(REPO, "translation", "ru_RU", rel), encoding="utf-8", newline="") as fh:
        return {r[0]: r[4] for r in csv.reader(fh) if len(r) > 4}


transform = load_transforms()
TUP = re.compile(
    r'\((?:"([^"]+)"|(\w+)), "([^"]+)",\s*("(?:[^"\\]|\\.)*"),\s*("(?:[^"\\]|\\.)*")\)'
    r'(,\s*#[^\n]*)?'
)

for pattern in sys.argv[1:]:
    for patch_path in sorted(glob.glob(os.path.join(HERE, "patches", pattern + ".py"))):
        name = os.path.basename(patch_path)[:-3]
        mod = importlib.import_module(f"patches.{name}")
        files = {t[0] for t in mod.PATCHES}
        current = {f: read_rows(f) for f in files}
        stats = {"keep": 0, "drop": 0, "rebase": 0}
        manual = []
        src = open(patch_path, encoding="utf-8").read()
        spans = []
        for m in TUP.finditer(src):
            rel = m.group(1) if m.group(1) is not None else getattr(mod, m.group(2))
            rid, old, new = m.group(3), m.group(4)[1:-1], m.group(5)[1:-1]
            cell = current[rel].get(rid)
            if cell is None:
                manual.append((rel, rid, old, "строки нет"))
                spans.append((m.start(), m.end(), m.group(0)))
                continue
            if cell == new:
                stats["drop"] += 1
                spans.append((m.start(), m.end(), None))
            elif cell == old:
                stats["keep"] += 1
                spans.append((m.start(), m.end(), m.group(0)))
            elif transform(old) == cell:
                stats["keep"] += 1
                stats["rebase"] += 1
                spans.append((m.start(), m.end(),
                              f'("{rel}", "{rid}",\n     "{cell}",\n     "{new}"){m.group(6) or ""}'))
            else:
                manual.append((rel, rid, old, f"в файле: {cell[:70]}"))
                spans.append((m.start(), m.end(), m.group(0)))
        out = src
        for s, e, rep in reversed(spans):
            out = out[:s] + ("" if rep is None else rep) + out[e:]
        out = re.sub(r"\n[ \t]+,(?=\n)", "", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
        open(patch_path, "w", encoding="utf-8").write(out)
        print(f"{name:12} оставить {stats['keep']:3} | снять {stats['drop']:2} | "
              f"пересобрано {stats['rebase']:2} | ручных {len(manual)}")
        for rel, rid, old, msg in manual:
            print("    !", rel.split("/")[-1], rid, "|", msg)
