#!/usr/bin/env python3
"""Проверка согласования рода от первого лица в русских переводах.

Пол берётся из tools/gender_registry.json:
  * named    — конкретный персонаж с фиксированным каноническим полом (M/F);
  * roles    — общая роль (医疗干员, 信使, 士兵 ...), пол определяется по сцене;
  * neutral  — группы/роботы/голоса, проверка не применяется;
  * ignore   — маскированный говорящий (？？？).

Для общих ролей важно различать:
  * разные эпизоды — это разные люди, расхождение допустимо (INFO);
  * один файл — скорее всего один и тот же человек, это ошибка (WARN).

    python3 tools/check_gender.py              # отчёт на экран
    python3 tools/check_gender.py --json       # полный отчёт в .cache/gender_report.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANG = REPO / "translation" / "ru_RU"
REGISTRY = Path(__file__).resolve().parent / "gender_registry.json"

# пары муж/жен для форм, которые могут agreeing с "я"
PAIRS = [
    ('был','была'),('стал','стала'),('пришёл','пришла'),('пришел','пришла'),
    ('ушёл','ушла'),('ушел','ушла'),('сказал','сказала'),('сделал','сделала'),
    ('мог','могла'),('знал','знала'),('видел','видела'),('хотел','хотела'),
    ('думал','думала'),('пошёл','пошла'),('пошел','пошла'),('увидел','увидела'),
    ('нашёл','нашла'),('нашел','нашла'),('вернулся','вернулась'),('остался','осталась'),
    ('решил','решила'),('получил','получила'),('узнал','узнала'),('забыл','забыла'),
    ('помог','помогла'),('устал','устала'),('привык','привыкла'),
    ('научился','научилась'),('оказался','оказалась'),('поговорил','поговорила'),
    ('спросил','спросила'),('ответил','ответила'),('попросил','попросила'),
    ('посмотрел','посмотрела'),('услышал','услышала'),('понял','поняла'),
    ('запомнил','запомнила'),('прочитал','прочитала'),('написал','написала'),
    ('взял','взяла'),('дал','дала'),('открыл','открыла'),('закрыл','закрыла'),
    ('ждал','ждала'),('искал','искала'),('спас','спасла'),('защитил','защитила'),
    ('убил','убила'),('принял','приняла'),('поймал','поймала'),('поднял','подняла'),
    ('почувствовал','почувствовала'),('надеялся','надеялась'),
    ('попробовал','попробовала'),('занимался','занималась'),('слушал','слушала'),
    ('смотрел','смотрела'),('работал','работала'),('жил','жила'),('бывал','бывала'),
    ('ездил','ездила'),('ходил','ходила'),('носил','носила'),('имел','имела'),
    ('терпел','терпела'),('боялся','боялась'),('стыдился','стыдилась'),
    ('гордился','гордилась'),('радовался','радовалась'),('удивлялся','удивлялась'),
    ('сердился','сердилась'),('смеялся','смеялась'),('плакал','плакала'),
    ('молчал','молчала'),('мешал','мешала'),('помнил','помнила'),
    ('предположил','предположила'),('счёл','сочла'),('счел','сочла'),
    ('странствовал','странствовала'),('сторожил','сторожила'),
    ('останавливался','останавливалась'),('покинул','покинула'),
    ('готов','готова'),('рад','рада'),('согласен','согласна'),('уверен','уверена'),
    ('должен','должна'),('обязан','обязана'),('виноват','виновата'),
    ('прав','права'),('нужен','нужна'),
]
FEM = {f.lower() for _m, f in PAIRS}
FORMS = re.compile(r'\b(' + '|'.join(sorted(FEM | {m.lower() for m, _f in PAIRS}, key=len, reverse=True)) + r')\b', re.I)
# "я" и глагол должны быть в одном предложении, между ними только наречия/частицы
SUBJ = re.compile(
    r'\bя\b(?:\s+(?:не|уже|очень|ещё|бы|тоже|всегда|никогда|просто|совсем|как|и|ну|уж|'
    r'конечно|даже|как-то|давно|сам|сама|одна|один|то|же|ли)){0,4}\s*$', re.I)
# если между "я" и формой есть другое подлежащее — это не самоописание
BLOCK = re.compile(
    r'\b(?:он|она|они|ты|вы|мы|кто|кто-то|никто|каждый|любой|человек|народ|doctor|доктор|'
    r'родос|суд|путь|пик|цикл|отец|мать|сестра|брат|группа|союз|армия|мага|приступ|выход|'
    r'дверь|сила|жизнь|огонь|флот|храм|колокол|бабушка|женщина|мужчина|комната|машина|смерть|'
    r'существо|гость|метод|итог|график|кампус|проект|отчёт|отчет|балл|журнал|случай|дневник|'
    r'пункт|ребёнок|ребенок|папа|дедушка|солдат|охранник|капитан|полковник|дух|протокол|'
    r'убийца|жена|семья|дети|способ|объём|объем|файл|карта|книга|меч|город|мастер|рыцарь|'
    r'приказ|результат|событие|время|день|ночь|утро|вечер|ветер|дождь|река|гора|море|'
    r'здание|стена|стол|стул|телефон|письмо|сообщение|организация|компания|школа|'
    r'университет|библиотека)\b', re.I)


def is_role(label: str, role_labels: list[str]) -> bool:
    return any(r in label for r in role_labels)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true', help='записать полный отчёт в .cache/gender_report.json')
    args = ap.parse_args()

    reg = json.loads(REGISTRY.read_text(encoding='utf-8'))
    named, neutral, ignore = reg['named'], set(reg['neutral']), set(reg['ignore_labels'])
    scene_overrides = reg['scene_overrides']

    hits = []
    for path in sorted(LANG.glob('story/**/*.csv')):
        rel = path.relative_to(LANG).as_posix()
        episode = rel.split('/')[1]
        for row in csv.reader(path.open(encoding='utf-8', newline='')):
            if not row or not row[0].startswith('line-') or len(row) < 5 or not row[1].strip():
                continue
            label = row[1]
            if label in ignore or label in neutral or label in scene_overrides:
                continue
            gender = named.get(label)
            role = is_role(label, reg['role_labels'])
            if gender is None and not role:
                continue
            for m in FORMS.finditer(row[4]):
                word = m.group(1).lower()
                left = row[4][max(0, m.start() - 60):m.start()]
                clause = re.split(r'[.!?;:\n]', left)[-1]
                ya = re.search(r'\bя\b', clause, re.I)
                if not ya or not SUBJ.search(clause):
                    continue
                if BLOCK.search(clause[ya.end():]):
                    continue
                actual = 'F' if word in FEM else 'M'
                hits.append({
                    'file': rel, 'episode': episode, 'id': row[0], 'label': label,
                    'kind': 'named' if gender in ('F', 'M') else 'role',
                    'expected': gender, 'actual': actual, 'word': word, 'text': row[4],
                })

    # 1) фиксированный пол персонажа
    conflicts = [h for h in hits if h['kind'] == 'named' and h['expected'] != h['actual']]
    # 2) общая роль: оба пола в одном файле
    by_file = collections.defaultdict(lambda: collections.defaultdict(set))
    by_role = collections.defaultdict(lambda: collections.defaultdict(set))
    for h in hits:
        if h['kind'] == 'role':
            by_file[h['file']][h['label']].add(h['actual'])
            by_role[h['label']][h['episode']].add(h['actual'])
    mixed_file = [(f, l, sorted(g)) for f, ls in by_file.items() for l, g in ls.items() if len(g) > 1]
    # оба пола внутри одного эпизода (даже если в разных файлах) — это уже ошибка
    mixed_episode = [(l, e, sorted(g)) for l, es in by_role.items() for e, g in es.items() if len(g) > 1]
    # только если пол различается между эпизодами — это разные люди, норма
    cross = []
    for l, es in by_role.items():
        allg = set().union(*es.values())
        if len(allg) > 1 and not any(len(g) > 1 for g in es.values()):
            cross.append((l, {e: sorted(g) for e, g in es.items()}))

    print(f'Просканировано реплик с известным полом: {len(hits)}')
    print(f'1. Именованные персонажи, род не совпадает с каноном: {len(conflicts)}')
    for h in conflicts[:40]:
        print(f'   {h["file"]} {h["id"]} {h["label"]}: {h["word"]} ({h["actual"]}), ждали {h["expected"]}')
    print(f'2. Общая роль с разным полом в ОДНОМ ФАЙЛЕ: {len(mixed_file)}')
    for f, l, g in mixed_file[:40]:
        print(f'   {f} {l}: {g}')
    print(f'3. Общая роль с разным полом в ОДНОМ ЭПИЗОДЕ: {len(mixed_episode)}')
    for l, e, g in sorted(mixed_episode)[:40]:
        print(f'   {l} в {e}: {g}')
    print(f'4. Разный пол ТОЛЬКО между эпизодами (разные люди, норма): {len(cross)}')
    for l, es in sorted(cross)[:40]:
        print(f'   {l}: {es}')

    if args.json:
        out = REPO / '.cache' / 'gender_report.json'
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps({
            'conflicts': conflicts, 'mixed_in_file': mixed_file,
            'mixed_in_episode': mixed_episode, 'cross_episode_ok': cross,
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'\nПолный отчёт: {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
