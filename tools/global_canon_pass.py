#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Глобальный канон-проход (решение NUM 2026-11-16).

1. В русском тексте не бывает апострофов: имена с апострофом возвращаются
   к канонической кириллической форме (Болдракасти, Кальцит, Хоолхейак,
   Вишадель, ...). Апострофы-кавычки переводятся в « ».
2. Если имя написано латиницей в оригинальном тексте (ZH), оно остаётся
   латиницей и в переводе (Raidian, Scout, Outcast, ...).
3. Компании: корректная транслитерация — «Пингвин Логистикс».

Меняется только русский текст: 5-я колонка CSV, поля titleRu/textRu досье,
RU-значения в канон-источниках. ID / Character / ZH / EN / служебные строки
и структура файлов не трогаются. Сохраняется исходный EOL.

    python3 tools/global_canon_pass.py            # dry-run
    python3 tools/global_canon_pass.py --apply
"""
from __future__ import annotations

import csv
import glob
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv

# --- 1. Апострофы в русских словах -> каноническая форма ------------------
# Порядок важен: сначала более длинные варианты.
APOSTROPHE_RULES: list[tuple[str, str]] = [
    (r"Кель'тейт", "Кальцит"),
    (r"Кель'тей", "Кальцит"),
    (r"Кель'сыйт", "Кальцит"),
    (r"Кель'цит", "Кальцит"),
    (r"Кель'сит", "Кальцит"),
    (r"Кель'си", "Кальцит"),
    (r"Кел'си", "Кальцит"),
    (r"Каль'цит", "Кальцит"),
    (r"Кал'цит", "Кальцит"),
    (r"Кэл'цит", "Кальцит"),
    (r"Калт'сит", "Кальцит"),
    (r"Кельци'с", "Кальцит"),
    (r"Бол'дракас", "Болдракасти"),
    (r"Хо'олхейак", "Хоолхейак"),
    (r"Хо'олхеяк", "Хоолхейак"),
    (r"ВИШ'АДЭЛЬ", "ВИШАДЕЛЬ"),
    (r"Виш'адэль", "Вишадель"),
    (r"Виш'адель", "Вишадель"),
    (r"Виш'эйдель", "Вишадель"),
    (r"Виш'дейл", "Вишадель"),
    (r"Виш'дэль", "Вишадель"),
    (r"Виш'дель", "Вишадель"),
    (r"Ч'ен", "Чэнь"),
    (r"Эл'ки", "Аргес"),
    (r"Бай'э", "Белый мел"),
    (r"Во'о", "Воо"),
    (r"Э'э", "Ээ"),
    (r"О'Брайен", "Обрайен"),
    (r"Mon3tr'а", "Mon3tr"),
    (r"лид'чоа", "lid'čoa"),  # ZH: lid'čoa — латиница, апостроф не русский
]

# Одиночные кавычки-пары -> ёлочки (только в русском тексте).
QUOTE_RULE = (r"'([^']{2,600})'", r"«\1»")

# Опечатка канонического термина Originium (сохраняет все падежные окончания).
TERM_RULES: list[tuple[str, str]] = [
    (r"Ориниум", "Ориджиниум"),
    (r"Тересис", "Терезис"),  # решение NUM: Терезис (муж.) ≠ Тереза (жен.)
    (r"(?<![А-Яа-яЁё])Каттус(?![А-Яа-яЁё])", "Каутус"),
    (r"(?<![А-Яа-яЁё])Катс(?![А-Яа-яЁё])", "Каутус"),
    (r"(?<![А-Яа-яЁё])Аледа(?![А-Яа-яЁё])", "Алердей"),
    # 圣骏堡 = Deity Grypherburg (яп. サンクト・グリファーブルク) — вымышленная
    # столица Урсуса. Это НЕ реальный Санкт-Петербург (решение NUM 2026-11-18,
    # по arknights.wiki.gg). Замена основы покрывает все падежи.
    (r"Санкт-Петербург", "Санкт-Грифербург"),
]

# --- 2b. Канонические имена и названия (без апострофов) -------------------
# Сведено по tools/UNIFY.md и glossary.json. Plain-варианты не покрывались
# APOSTROPHE_RULES, поэтому оставались в st/ и части event-эпизодов.
CANON_NAME_RULES: list[tuple[str, str]] = [
    (r"Кельси", "Кальцит"),                      # 凯尔希
    (r"Кложур", "Кложер"),                        # 可露希尔
    (r"Клозур", "Кложер"),
    (r"Клозер", "Кложер"),
    (r"Клоссир", "Кложер"),
    (r"Клосс", "Кложер"),
    (r"Клозир", "Кложер"),
    (r"Клозиер", "Кложер"),
    (r"Клози(?!р|е)", "Кложер"),
    (r"Реюниона", "Воссоединения"),                # 整合运动 (склонение)
    (r"Реюниону", "Воссоединению"),
    (r"Реюнионом", "Воссоединением"),
    (r"Реюнионе", "Воссоединении"),
    (r"Реюнион", "Воссоединение"),
    (r"Таллула", "Талула"),                       # 塔露拉
    (r"Острова Родос", "Родоса"),                 # 罗德岛 (родительный)
    (r"Остров Родос", "Родос"),                   # 罗德岛
    (r"Королева Истребления", "Сидж"),             # 推进之王
    (r"Король Сигнал", "Сидж"),
    (r"Королева Сигнал", "Сидж"),
    (r"Чёрная Змея", "Чёрный Змей"),               # 黑蛇 — мужского рода
    (r"Чёрной Змеи", "Чёрного Змея"),
]

# --- 3. Компании ---------------------------------------------------------
COMPANY_RULES: list[tuple[str, str]] = [
    (r"Пингвин\s+Лоджистикс", "Пингвин Логистикс"),
    (r"Пингвин\s+Лоджистик(?!с)", "Пингвин Логистикс"),
    (r"Пингвин\s+Логистик(?!с)", "Пингвин Логистикс"),
    (r"Penguin\s+Logistics", "Пингвин Логистикс"),
]

# Организации, у которых канон сайта уже даёт русскую транслитерацию.
# Применяем, только если в ZH нет латинского написания (тогда Rule 2).
COMPANY_LATIN_TO_RU: list[tuple[str, str]] = [
    ("Blacksteel Worldwide", "Блэкстил Ворлдвайд"),
    ("Rhodes Island", "Родос"),
    ("Rhine Lab", "Рейн Лаб"),
    ("Blacksteel", "Блэкстил"),
]

# --- 2. Латиница в ZH остаётся латиницей в RU ---------------------------
# Имя в ZH -> список кириллических вариантов, которые надо вернуть к латинице.
LATIN_FROM_ZH: dict[str, list[str]] = {
    "Raidian": [r"Рэйдиан[А-Яа-яЁё]*", r"Рэдиан[А-Яа-яЁё]*", r"Райдиан[А-Яа-яЁё]*",
                r"Рейдиан[А-Яа-яЁё]*", r"Редиан[А-Яа-яЁё]*", r"Радиан[А-Яа-яЁё]*"],
    "Scout": [r"Скаут[А-Яа-яЁё]*"],
    "Misery": [r"Майзери", r"Мизари", r"Мизери"],
    "Outcast": [r"Ауткаст[А-Яа-яЁё]*", r"Аутсайдер[А-Яа-яЁё]*"],
    "Mantra": [r"Мантра[А-Яа-яЁё]*"],
    "Sharp": [r"Шарп[А-Яа-яЁё]*"],
    "Guard": [r"Гард[А-Яа-яЁё]*"],
    "Mechanist": [r"Механист[А-Яа-яЁё]*"],
    "Ace": [r"Эйс[А-Яа-яЁё]*"],
    "Alty": [r"Алти", r"Олти"],
    "Mon3tr": [r"Мон3стр[А-Яа-яЁё]*", r"Мон3тр[А-Яа-яЁё]*", r"Монстр[А-Яа-яЁё]*"],
    "Logos": [r"Logos[А-Яа-яЁё]+"],
    "Christine": [r"Кристин[А-Яа-яЁё]*"],
    "Frost": [r"Фрост[А-Яа-яЁё]*"],
    "Lancet-2": [r"Ланцет-2"],
    "Ishar-mla": [r"Ишар\s+мла"],
}

stats: Counter = Counter()
samples: dict[str, str] = {}


def note(tag: str, before: str, after: str, where: str) -> None:
    stats[tag] += 1
    samples.setdefault(tag, f"{where}: {before[:70]!r} -> {after[:70]!r}")


def fix_ru(text: str, zh: str = "", where: str = "") -> str:
    """Применяет все правила к русскому тексту. zh — оригинал для условия #2."""
    out = text
    for pat, rep in APOSTROPHE_RULES:
        new = re.sub(pat, rep, out)
        if new != out:
            note("апостроф", out, new, where)
            out = new
    new = re.sub(QUOTE_RULE[0], QUOTE_RULE[1], out)
    if new != out:
        note("кавычки", out, new, where)
        out = new
    for pat, rep in TERM_RULES:
        new = re.sub(pat, rep, out)
        if new != out:
            note(f"термин:{rep}", out, new, where)
            out = new
    for pat, rep in CANON_NAME_RULES:
        new = re.sub(pat, rep, out)
        if new != out:
            note(f"имя:{rep}", out, new, where)
            out = new
    for pat, rep in COMPANY_RULES:
        new = re.sub(pat, rep, out, flags=re.IGNORECASE if pat.startswith("Penguin") else 0)
        if new != out:
            note("компания", out, new, where)
            out = new
    for latin, ru in COMPANY_LATIN_TO_RU:
        if latin in out and not (zh and re.search(re.escape(latin), zh, re.I)):
            new = out.replace(latin, ru)
            note(f"компания:{latin}", out, new, where)
            out = new
    if zh:
        for name, pats in LATIN_FROM_ZH.items():
            # имя должно стоять отдельным словом, но не быть частью Mon3tr
            zh_pat = r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])"
            if not re.search(zh_pat, zh):
                continue
            for pat in pats:
                new = re.sub(pat, name, out)
                if new != out:
                    note(f"латиница:{name}", out, new, where)
                    out = new
        # Mon (не Mon3tr) — отдельным словом
        if re.search(r"(?<![A-Za-z0-9])Mon(?![A-Za-z0-9])", zh):
            new = re.sub(r"(?<![А-Яа-яЁё0-9])Мон(?![А-Яа-яЁё0-9])", "Mon", out)
            if new != out:
                note("латиница:Mon", out, new, where)
                out = new
    return out


# --- CSV: только 5-я колонка ---------------------------------------------
csv_files = 0
csv_rows = 0
for path in sorted(REPO.glob("translation/ru_RU/**/*.csv")):
    raw = path.read_text(encoding="utf-8", newline="")
    eol = "\r\n" if "\r\n" in raw else "\n"
    rows = list(csv.reader(raw.splitlines(keepends=True)))
    dirty = False
    for row in rows:
        if len(row) < 5:
            continue
        zh = row[2] if len(row) > 2 else ""
        new = fix_ru(row[4], zh, f"{path.relative_to(REPO)}:{row[0]}")
        if new != row[4]:
            row[4] = new
            csv_rows += 1
            dirty = True
    if dirty:
        csv_files += 1
        if APPLY:
            buf = io.StringIO()
            csv.writer(buf, lineterminator=eol).writerows(rows)
            path.write_text(buf.getvalue(), encoding="utf-8", newline="")

# --- Досье: RU-поля JSON и рабочие .txt ---------------------------------
dossier_files = 0
for path in sorted(REPO.glob("translation/ru_RU/dossiers/*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    dirty = False
    for sec in data.get("sections", []):
        for key in ("titleRu", "textRu"):
            if key not in sec or not isinstance(sec[key], str):
                continue
            new = fix_ru(sec[key], where=f"dossier:{path.name}:{key}")
            if new != sec[key]:
                sec[key] = new
                dirty = True
    if dirty:
        dossier_files += 1
        if APPLY:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1).rstrip("\n"), encoding="utf-8")

txt_files = 0
for path in sorted(REPO.glob(".cache/dossiers/ru/*.txt")):
    raw = path.read_text(encoding="utf-8")
    new = fix_ru(raw, where=f"txt:{path.name}")
    if new != raw:
        txt_files += 1
        if APPLY:
            path.write_text(new, encoding="utf-8")

print("режим:", "ПРИМЕНЕНИЕ" if APPLY else "dry-run (без записи)")
print(f"CSV: {csv_rows} строк в {csv_files} файлах")
print(f"досье JSON: {dossier_files} файлов | рабочие txt: {txt_files} файлов")
for tag, n in stats.most_common():
    print(f"  {n:4}  {tag:22} {samples[tag]}")
