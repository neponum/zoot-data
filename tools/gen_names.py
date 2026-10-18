#!/usr/bin/env python3
"""Расширяет реестр подписей говорящих в translation/ru_RU/glossary.json.

Источники (в порядке приоритета снизу вверх):
  1. существующие ручные записи в glossary.json — не перетираются;
  2. src/data/operator_names_map.json приложения (CN → RU, 441 персонаж);
  3. эвристики по общим ярлыкам безымянных NPC.

    python3 tools/gen_names.py --operator-map /путь/к/operator_names_map.json
    python3 tools/gen_names.py --operator-map ... --apply
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GLOSSARY = REPO / "translation" / "ru_RU" / "glossary.json"
DEFAULT_MAP = Path("/media/num/Something/NUM/ZOOT-ARCHIVE/src/data/operator_names_map.json")

# Общие ярлыки: китайская подпись → каноническая русская.
# A/B/C-суффиксы обрабатываются автоматически (латинская буква → кириллица).
COMMON = {
    "村民": "Житель деревни",
    "镇民": "Горожанин",
    "市民": "Горожанин",
    "路人": "Прохожий",
    "工人": "Рабочий",
    "士兵": "Солдат",
    "军官": "Офицер",
    "警察": "Полицейский",
    "赏金猎人": "Охотник за головами",
    "整合运动": "Участник Воссоединения",
    "整合运动成员": "Участник Воссоединения",
    "整合运动士兵": "Боец Воссоединения",
    "整合运动战士": "Боец Воссоединения",
    "整合运动术师": "Боец Воссоединения",
    "罗德岛干员": "Оперативник Родос Айленд",
    "罗德岛近卫干员": "Гвардеец Родос Айленд",
    "企鹅物流": "Пингвин Лоджистик",
    "黑钢国际": "Блэкстил",
    "企鹅物流快递员": "Курьер Пингвин Лоджистик",
    "敌人": "Противник",
    "干员": "Оперативник",
    "医疗干员": "Медик",
    "狙击干员": "Снайпер",
    "近卫干员": "Гвардеец",
    "重装干员": "Защитник",
    "辅助干员": "Саппорт",
    "特种干员": "Специалист",
    "术师干员": "Кастер",
    "先锋干员": "Авангард",
}

LETTER_MAP = str.maketrans({"A": "А", "B": "Б", "C": "В", "D": "Г", "E": "Д", "F": "Е"})


def with_letters(cn: str, ru: str) -> dict[str, str]:
    """阿达克利斯人A → Адаклис А (постфикс-буква кириллицей)."""
    if not cn or cn[-1] not in "ABCDEF":
        return {}
    letter = cn[-1].translate(LETTER_MAP)
    return {cn: f"{ru} {letter}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--operator-map", default=str(DEFAULT_MAP))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    gloss = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    entries: dict[str, str] = dict(gloss["names"]["entries"])
    before = dict(entries)

    # 1. оперативники
    if Path(args.operator_map).is_file():
        data = json.loads(Path(args.operator_map).read_text(encoding="utf-8"))
        seen: dict[str, str] = {}
        for value in data.values():
            cn = (value.get("chineseName") or "").strip()
            ru = (value.get("russianName") or "").strip()
            if cn and ru:
                seen.setdefault(cn, ru)
        for cn, ru in seen.items():
            if cn not in entries:
                entries[cn] = ru
                entries.update({k: v for k, v in with_letters(cn, ru).items() if k not in entries})
    else:
        print(f"! не найден operator_names_map.json: {args.operator_map}")

    # 2. общие ярлыки
    for cn, ru in COMMON.items():
        if cn not in entries:
            entries[cn] = ru
            entries.update({k: v for k, v in with_letters(cn, ru).items() if k not in entries})

    added = {k: v for k, v in entries.items() if k not in before}
    changed = {k: (before[k], v) for k, v in entries.items() if k in before and before[k] != v}

    for k, v in list(changed.items())[: args.limit]:
        print(f"  ПЕРЕОПРЕДЕЛЁН {k}: {changed[k][0]} → {changed[k][1]}")
    print(f"\nдобавлено записей: {len(added)}, переопределено: {len(changed)}")
    for k, v in list(added.items())[: args.limit]:
        print(f"  + {k} → {v}")
    if len(added) > args.limit:
        print(f"  … ещё {len(added) - args.limit}")

    if args.apply:
        gloss["names"]["entries"] = dict(sorted(entries.items()))
        GLOSSARY.write_text(json.dumps(gloss, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nзаписано в {GLOSSARY}: всего записей {len(entries)}")
    else:
        print("\ndry-run (без записи)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())