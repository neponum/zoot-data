# -*- coding: utf-8 -*-
"""Добивочный канон main глава 10: 卡特斯 / Cautus -> Каутус.

Все вхождения «Каттус»/«каттус» в 5-й колонке main_10 приведены к канону
расы «Каутус» (решение батча 12, UNIFY: Small Cautus = каута; main_15).
Падежи и согласование сохраняются (Каттус — неизменяемое слово).
深池/Sudean: «Сардин» оставлен без изменений по решению пользователя.

Применение: python3 tools/apply_patch.py main_10_canon [--apply]
"""
PATCHES = [
    ('main/level_main_10-03_end_nep0num.csv', 'line-533', 'Каттус', 'Каутус'),
    ('main/level_main_10-04_beg_nep0num.csv', 'line-65', 'Каттус', 'Каутус'),
    ('main/level_main_10-04_beg_nep0num.csv', 'line-73', 'Каттус', 'Каутус'),
    ('main/level_main_10-04_beg_nep0num.csv', 'line-462', 'Каттус', 'Каутус'),
    ('main/level_main_10-04_end_nep0num.csv', 'line-501', 'Каттус', 'Каутус'),
    ('main/level_main_10-05_beg_nep0num.csv', 'line-299', 'Каттус', 'Каутус'),
    ('main/level_main_10-05_beg_nep0num.csv', 'line-326', 'каттус', 'каутус'),
    ('main/level_main_10-06_beg_nep0num.csv', 'line-188', 'Каттус', 'Каутус'),
    ('main/level_main_10-08_end_nep0num.csv', 'line-441', 'Каттус', 'Каутус'),
    ('main/level_main_10-08_end_nep0num.csv', 'line-447', 'Каттус', 'Каутус'),
    ('main/level_main_10-12_end_nep0num.csv', 'line-160', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_beg_nep0num.csv', 'line-440', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_beg_nep0num.csv', 'line-475', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_end_nep0num.csv', 'line-311', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_end_nep0num.csv', 'line-959', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_end_nep0num.csv', 'line-1286', 'Каттус', 'Каутус'),
    ('main/level_main_10-15_end_nep0num.csv', 'line-1334', 'Каттус', 'Каутус'),
]
