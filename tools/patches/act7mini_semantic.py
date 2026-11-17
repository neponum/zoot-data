# -*- coding: utf-8 -*-
"""Полная построчная смысловая вычитка act7mini (RU <-> ZH <-> EN).

Все 1944 строки `line-N` в шести CSV просмотрены по трём колонкам.
Правки затронули только 5-ю колонку (Translation). Категории:

  - смысл: подмена времени («大清早» -> «среди бела дня»),
    «死得完整一点» -> «лёгкая смерть», «有没有他们» -> «примут нас»,
    «在乎» -> «интересно», «良心» -> «разум», «怪谈» -> «монстры»;
  - имена/термины: неверная страна «Латерано» вместо «Лейтания»,
    «Джейн» вместо «Дегенбрехер», саргонская брань вместо сарказской,
    «Клиффхарт» там, где в ZH/EN «Энсия», «госпожа» вместо «мисс»,
    «天灾» -> «Катастрофа», «城市» -> «деревня»;
  - опечатки: «шлём» -> «шлем», «показалось. Кристалл» -> «выглядывает кристалл».

Применение: python3 tools/apply_patch.py act7mini_semantic [--apply]
"""

PATCHES = [
    # ---- st01 ----
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-243',
     'Никому *чертовски* не интересно.', 'Никого *чертовски* не волнует.'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-362',
     'примут они нас или нет', 'есть они или нет'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-376',
     'Бедствия раз за разом проходились по земле',
     'Катастрофы раз за разом проходились по земле'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-401',
     'среди бела дня', 'так рано утром'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-512',
     'Не так активно, звучит', 'Не горячись, звучит'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-547',
     'я обещаю, что смерть будет легкой.', 'я обещаю, что умрёшь целым.'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-583',
     'шлём', 'шлем'),
    ('act7mini/level_act7mini_st01_nep0num.csv', 'line-634',
     'Бедствие проходит по Пустошам', 'Катастрофа проходит по Пустошам'),

    # ---- st02 ----
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-8',
     'Этому месту больше нет дела до твоего существования.',
     'Здесь тебе больше не найти приюта.'),
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-94',
     'вынуждая их нарушить голос разума',
     'вынуждая их подчиниться голосу совести'),
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-307',
     '*саргонское ругательство*', '*сарказское ругательство*'),
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-323',
     'Самый известный город Акроти', 'Самая известная деревня Акроти'),
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-367',
     '(Топот)', '(Наступает на ногу)'),
    ('act7mini/level_act7mini_st02_nep0num.csv', 'line-516',
     '*Саргонское ругательство*', '*Сарказское ругательство*'),

    # ---- st03 ----
    ('act7mini/level_act7mini_st03_nep0num.csv', 'line-416',
     'стихийным бедствием', 'Катастрофой'),
    ('act7mini/level_act7mini_st03_nep0num.csv', 'line-455',
     'превратить восток в рай для монстров',
     'превратить Хигаси в рай городских легенд'),
    ('act7mini/level_act7mini_st03_nep0num.csv', 'line-474',
     'Супер сбылось!', 'Я просто в восторге!'),
    ('act7mini/level_act7mini_st03_nep0num.csv', 'line-541',
     'Вали обратно в свою Латерано.', 'Вали обратно в свою Лейтанию.'),

    # ---- st04 ----
    ('act7mini/level_act7mini_st04_nep0num.csv', 'line-223',
     'К привычкам сложно привыкнуть.', 'Привычки трудно изменить.'),

    # ---- st05: обращение к женщине по канону — «мисс» (EN: Miss Carnelian) ----
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-11',
     'Госпожа Карнелиан', 'Мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-41',
     'Госпожа Карнелиан', 'Мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-53',
     'Госпожа Карнелиан', 'Мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-60',
     'Госпожа Карнелиан', 'Мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-74',
     'госпожа Карнелиан', 'мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-106',
     'госпожа Карнелиан', 'мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-115',
     'госпожа Карнелиан', 'мисс Карнелиан'),
    ('act7mini/level_act7mini_st05_nep0num.csv', 'line-304',
     'у ворота, показалось. Кристалл.', 'у ворота выглядывает кристалл.'),

    # ---- st06 ----
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-158',
     'госпожи Джейн', 'госпожи Дегенбрехер'),
    # В ZH/EN в этих репликах имя «恩希亚 / Lady Ensia», а не «崖心 / Cliffheart»
    # (в первой половине эпизода тот же персонаж уже переведён как «Энсия»).
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-295',
     'Мисс Клиффхарт', 'Мисс Энсия'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-297',
     ' Мисс Клиффхарт это', ' Мисс Энсия это'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-304',
     'мисс Клиффхарт не из тех', 'мисс Энсия не из тех'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-339',
     'для мисс Клиффхарт', 'для мисс Энсии'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-353',
     'мисс Клиффхарт не знакома', 'мисс Энсия не знакома'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-364',
     'мисс Клиффхарт, ваша решимость', 'мисс Энсия, ваша решимость'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-372',
     'Мисс Клиффхарт, вы собираетесь', 'Мисс Энсия, вы собираетесь'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-435',
     'вас, мисс Клиффхарт, лезущей', 'вас, мисс Энсия, лезущей'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-447',
     'Мисс Клиффхарт всегда', 'Мисс Энсия всегда'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-455',
     'мисс Клиффхарт.', 'мисс Энсия.'),
    ('act7mini/level_act7mini_st06_nep0num.csv', 'line-541',
     'мисс Клиффхарт, вот вещь', 'мисс Энсия, вот вещь'),
]
