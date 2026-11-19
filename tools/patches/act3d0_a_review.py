# -*- coding: utf-8 -*-
""" act3d0, первая половина (12 CSV, 723 реплики): полная смысловая сверка RU <-> ZH <-> EN. """

PATCHES = [
    # ── level_act3d0_st01_nep0num.csv ──────────────────────────────────────
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-17',
     'Мисс Сейлон, по-пожалуйста, успокойтесь.',
     'Мисс Цейлон, пожалуйста, успокойтесь.'),                                  # имя + опечатка
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-25',
     'придется рассчитывать', 'придётся рассчитывать'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-30',
     'начнется фестиваль', 'начнётся фестиваль'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-139',
     'придется ещё', 'придётся ещё'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-150',
     'Эй, Со?', 'Эй, Сора?'),                                                   # 空 = Сора
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-159',
     'становится тяжеловато', 'становится тяжёловато'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-173',
     'вся ты, Со.', 'вся ты, Сора.'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-184',
     'посла бедствий города', 'вестника Катастрофы города'),                    # 天灾信使
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-196',
     'как посланник бедствий', 'как вестник Катастрофы'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-220',
     'вестник бедствий говорил', 'вестник Катастрофы говорил'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-232',
     'Скайфаер, Прованс!', 'Скайфайр, Прованс!'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-237',
     'Прованс и Скайфаер?', 'Прованс и Скайфайр?'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-244',
     'Скайфаер просто', 'Скайфайр просто'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-245',
     'вестник бедствий, уже', 'вестник Катастрофы, уже'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-249',
     'Скайфаер, даже', 'Скайфайр, даже'),
    ('story/act3d0/level_act3d0_st01_nep0num.csv', 'line-316',
     'что-нибудь легкое!', 'что-нибудь лёгкое!'),

    # ── level_act3d0_06_beg_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-11',
     'начнется через 3 часа', 'начнётся через 3 часа'),
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-45',
     'Мисс Сайланс', 'Мисс Цейлон'),
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-47',
     'Если мы этого не сделаем, все жители Сиесты пострадают.',
     'Если я этого не сделаю, все жители Сиесты пострадают.'),                  # 如果不这么做 — «я»
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-62',
     'Мисс Сайланс', 'Мисс Цейлон'),
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-104',
     'о твоем прошлом', 'о твоём прошлом'),
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-118',
     'помощь Сайланс', 'помощь Цейлон'),
    ('story/act3d0/level_act3d0_06_beg_nep0num.csv', 'line-138',
     'возможно, придется отменить', 'возможно, придётся отменить'),

    # ── level_act3d0_ex03_end_nep0num.csv ──────────────────────────────────
    ('story/act3d0/level_act3d0_ex03_end_nep0num.csv', 'line-68',
     'молодой завра', 'молодой савра'),                                          # 萨弗拉 = Савра
    ('story/act3d0/level_act3d0_ex03_end_nep0num.csv', 'line-95',
     'Эй, завра, не прогоняй', 'Эй, савра, не прогоняй'),
    ('story/act3d0/level_act3d0_ex03_end_nep0num.csv', 'line-109',
     'Если бы я тогда не вмешался, скольких ещё',
     'Если бы я не был вам так не по душе, скольких ещё'),                       # 看不顺眼 ≠ вмешательство

    # ── level_act3d0_st04_nep0num.csv ──────────────────────────────────────
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-13',
     'трансляция скоро начнется', 'трансляция скоро начнётся'),
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-31',
     'но я должен сказать вам', 'но я должна сказать вам'),                     # D.D.D. — женщина
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-49',
     'Силен рассказала мне', 'Цейлон рассказала мне'),
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-74',
     'о своем отъезде из города, поручив Чёрной расследовать все под прикрытием',
     'о своём отъезде из города, поручив Шварц расследовать всё под прикрытием'),
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-81',
     'Дедушка Хелаг, вы', 'Дедушка Хеллагур, вы'),
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-107',
     'почему я подгораю?', 'почему у меня подгорает?'),                          # 烤糊了 — подгорает еда
    ('story/act3d0/level_act3d0_st04_nep0num.csv', 'line-108',
     'Дядя Матерхорн!', 'Дядя Маттерхорн!'),

    # ── level_act3d0_ex01_end_nep0num.csv — правок нет ──────────────────────

    # ── level_act3d0_01_end_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-24',
     '«Исследование ориниума»', '«Исследование Ориджиниума»'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-30',
     'ученый обязан', 'учёный обязан'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-32',
     'Вернемся к тому', 'Вернёмся к тому'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-47',
     'Провенанс, она', 'Прованс, она'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-56',
     'как о чем-то', 'как о чём-то'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-69',
     'Ты только что чуть не пострадала от ориниумных жуков',
     'Ты только что была атакована ориджиниевыми жуками'),                       # 被…袭击了 — не «чуть не»
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-72',
     'ориниумные жуки', 'ориджиниевые жуки'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-80',
     'Провенанс, похоже', 'Прованс, похоже'),
    ('story/act3d0/level_act3d0_01_end_nep0num.csv', 'line-93',
     'озверевшие ориниумные жуки', 'озверевшие ориджиниевые жуки'),

    # ── level_act3d0_07_end_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-19',
     'неужели легкое землетрясение', 'неужели лёгкое землетрясение'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-31',
     'что разберетесь в ситуации', 'что разберётесь в ситуации'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-49',
     'Анализ вулкана завершен!', 'Анализ вулкана завершён!'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-60',
     'Блэк, дедушка Хеллаг', 'Шварц, дедушка Хеллагур'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-66',
     'Сейлон...', 'Цейлон...'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-69',
     'Курьеры бедствий, вулканологи', 'Вестники Катастрофы, вулканологи'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-70',
     'Как курьер бедствий', 'Как вестник Катастрофы'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-72',
     'такой серьезности', 'такой серьёзности'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-74',
     'Мгм. Блэк, ты тоже иди.', 'Мгм. Шварц, ты тоже иди.'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-78',
     'Сейлон сказала', 'Цейлон сказала'),
    ('story/act3d0/level_act3d0_07_end_nep0num.csv', 'line-94',
     'половина Сиесты', 'большая часть Сиесты'),                                 # 大半座 ≠ половина

    # ── level_act3d0_01_beg_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-14',
     'мисс Эйяфьядле', 'мисс Эйяфьяллле'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-19',
     'Хотя ты и сама Вестник катастроф, только мой багаж знаний может гарантировать, что вы не попадете в неприятности',
     'Хотя ты и сама вестник Катастрофы, только мой багаж знаний может гарантировать, что вы не попадёте в неприятности'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-23',
     'придется создавать', 'придётся создавать'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-31',
     'огнем!', 'огнём!'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-55',
     'Объемы выбросов вулканических газов выше, чем я предполагала, и руны обнаружения, переданные мне Эйяфьядлой, уже отреагировали.',
     'Объёмы выбросов вулканических газов выше, чем я предполагала, и руны обнаружения, переданные мне Эйяфьяллой, уже отреагировали.'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-56',
     'ничего не придется, скоро', 'ничего не придётся, скоро'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-59',
     'мисс Эйяфьядлу', 'мисс Эйяфьяллу'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-76',
     'У Эйяфьядлы', 'У Эйяфьяллы'),
    ('story/act3d0/level_act3d0_01_beg_nep0num.csv', 'line-88',
     'Черт, подол', 'Чёрт, подол'),

    # ── level_act3d0_04_end_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_04_end_nep0num.csv', 'line-39',
     'Дедушка Хелаг,', 'Дедушка Хеллагур,'),
    ('story/act3d0/level_act3d0_04_end_nep0num.csv', 'line-44',
     'когда Блэк заботилась', 'когда Шварц заботилась'),
    ('story/act3d0/level_act3d0_04_end_nep0num.csv', 'line-47',
     'Как Блэк может', 'Как Шварц может'),
    ('story/act3d0/level_act3d0_04_end_nep0num.csv', 'line-48',
     'за Кронингом стоит', 'за Кронином стоит'),

    # ── level_act3d0_07_beg_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-19',
     'Гость на месте,', 'Гости на местах,'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-27',
     'подчиненные, которых я привлек за последние годы. Только они знают, что такое награда, заработанная тяжелым трудом',
     'подчинённые, которых я привлёк за последние годы. Только они знают, что такое награда, заработанная тяжёлым трудом'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-33',
     'Систа и вправду', 'Сиеста и вправду'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-37',
     'вестником бедствий этого города', 'вестником Катастрофы этого города'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-38',
     'как Систа превращается', 'как Сиеста превращается'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-39',
     'извержении вулкана Систа.', 'извержении вулкана Сиеста.'),
    ('story/act3d0/level_act3d0_07_beg_nep0num.csv', 'line-49',
     'ценность Систы в своем лицемерии', 'ценность Сиесты в своём лицемерии'),
    # ── level_act3d0_04_beg_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_04_beg_nep0num.csv', 'line-9',
     'Отряды А и Б, держите дистанцию. Отряд С, заходите в тыл.',
     'Отряды А и Б, держитесь поодаль и следите внимательно. Отряд С, заходите в тыл.'),  # 远处盯紧了
    ('story/act3d0/level_act3d0_04_beg_nep0num.csv', 'line-49',
     'обманули мисс Силланг.', 'обманули мисс Цейлон.'),

    # ── level_act3d0_02_end_nep0num.csv ────────────────────────────────────
    ('story/act3d0/level_act3d0_02_end_nep0num.csv', 'line-24',
     'что случилось с Кронингом!?', 'что случилось с Кронином!?'),
    ('story/act3d0/level_act3d0_02_end_nep0num.csv', 'line-27',
     'слушаться Кронинга.', 'слушаться Кронина.'),
    ('story/act3d0/level_act3d0_02_end_nep0num.csv', 'line-31',
     'обратно к Кронингу', 'обратно к Кронину'),
]
