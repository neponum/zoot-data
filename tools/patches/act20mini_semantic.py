# -*- coding: utf-8 -*-
"""Полная построчная смысловая сверка RU <-> ZH (EN = ZH в этом эпизоде).

Исправлены: сдвиг трёх реплик в st01, смысловые ошибки (无酒精 -> без алкоголя,
后天 -> послезавтра, 银枪天马 -> «Серебряный Пегас», ориниум -> ориджиниум),
а также канонические/внутренние несогласованности имён и терминов.
"""

PATCHES = [
    # --- st01 ---
    # канон UNIFY: 沙雷 -> Салей (не «Сале»)
    ('act20mini/level_act20mini_st01_nep0num.csv', 'line-591',
     'господин Сале.', 'господин Салей.'),
    # сдвиг перевода на три строки: line-696 содержал только «...»,
    # текст line-696 лежал в line-697, а text line-697+698 — в line-698
    ('act20mini/level_act20mini_st01_nep0num.csv', 'line-696',
     '...', 'Нет. Просто у меня появилось чувство, что, возможно, Новый Вольсиний в итоге все ещё остается городом Сиракуз.'),
    ('act20mini/level_act20mini_st01_nep0num.csv', 'line-697',
     'Нет. Просто у меня появилось чувство, что, возможно, Новый Вольсиний в итоге все ещё остается городом Сиракуз.',
     'Может, что-то и изменилось, а может, в конечном счёте ничего не изменилось вовсе.'),
    ('act20mini/level_act20mini_st01_nep0num.csv', 'line-698',
     'Может, что-то и изменилось, а может, в конечном счёте ничего не изменилось вовсе. Или, может, что-то, что было неизменным, попало в этот новый мир и породило нечто совсем иное.',
     'Или, может, что-то, что было неизменным, попало в этот новый мир и породило нечто совсем иное.'),

    # --- st02 ---
    # UNIFY: 银枪天马 / A Silverlance Pegasus -> «Серебряный Пегас»
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-95',
     'Серебряного копья', '„Серебряного Пегаса“'),
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-103',
     'Серебряного копья', '«Серебряного Пегаса»'),
    # опечатка: Лейтания
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-137',
     'лертанийцам', 'лейтанийцам'),
    # 无酒精 = безалкогольный, а не «без сахара»
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-138',
     'без сахара', 'без алкоголя'),
    # единообразие названия закона (ед. число, как в остальных главах)
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-158',
     'новыми городами', 'Новым городом'),
    ('act20mini/level_act20mini_st02_nep0num.csv', 'line-738',
     'без сахара', 'без алкоголя'),

    # --- st03 --- единообразие транслитерации 维尔蒂 -> Верти
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-42', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-49', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-63', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-79', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-94', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-107', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-343', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-417', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-421', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-464', 'Вильди', 'Верти'),
    ('act20mini/level_act20mini_st03_nep0num.csv', 'line-567', 'Вильди', 'Верти'),

    # --- st04 ---
    # 源石 = Ориджиниум (канон), опечатка «ориниум»
    ('act20mini/level_act20mini_st04_nep0num.csv', 'line-63',
     'ориниума', 'ориджиниума'),

    # --- st05 --- единообразие: Лейтания / лейтанийский
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-173',
     'летанском', 'лейтанийском'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-217',
     'Мы же как и Паула, приехали из Летании, может, они вообще целенаправленно против нас, летанцев?',
     'Мы же как и Паула, приехали из Лейтании, может, они вообще целенаправленно против нас, лейтанийцев?'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-260',
     'покинула Летанию', 'покинула Лейтанию'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-265',
     'из Летании', 'из Лейтании'),
    # 后天 = послезавтра, а не «завтра»
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-269',
     'что завтра она наденет', 'что послезавтра она наденет'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-297',
     'всех летанцев в Сиракузах', 'всех лейтанийцев в Сиракузах'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-336',
     'на летанском', 'на лейтанийском'),
    ('act20mini/level_act20mini_st05_nep0num.csv', 'line-338',
     'на летанском', 'на лейтанийском'),

    # --- st06 --- канон UNIFY: 沙雷 -> Салей (с согласованием падежей)
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-105',
     'Господин Шаре,', 'Господин Салей,'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-119',
     'Господин Шаре,', 'Господин Салей,'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-157',
     '«Золотой равнине» Шаре', '«Золотой равнине» Салея'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-158',
     'Шаре преследует', 'Салей преследует'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-160',
     'за спиной Шаре', 'за спиной Салея'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-175',
     'продвигаемые Шаре', 'продвигаемые Салеем'),
    # единообразие: 运输保障署 -> Бюро транспортного обеспечения
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-179',
     'наше Агентство по обеспечению перевозок при правительстве',
     'наше Бюро транспортного обеспечения при правительстве'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-234',
     'как Шаре и Торговой федерации', 'как Салею и Торговой федерации'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-247',
     'торговца Шаре', 'торговца Салея'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-271',
     'из Агентства по обеспечению перевозок', 'из Бюро транспортного обеспечения'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-277',
     'другого сотрудника Агентства', 'другого сотрудника Бюро'),
    # единообразие транслитерации 维尔蒂 -> Верти
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-407', 'Верди', 'Верти'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-409', 'Верди', 'Верти'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-413', 'Верди', 'Верти'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-437', 'Верди', 'Верти'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-340',
     '«Чёрная завеса»', '«Чёрный бархат»'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-570',
     'Господин Шаре,', 'Господин Салей,'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-659',
     'Шаре? Зачем', 'Салей? Зачем'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-668',
     'Шаре пришел', 'Салей пришел'),
    # UNIFY: 西西里夫人 -> Синьора Сицилия
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-751',
     'госпожой Сицилией', 'синьорой Сицилией'),
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-753',
     'эту госпожу', 'эту синьору'),
    # 铳与秩序 = «Оружие и Порядок» (канон из act21side)
    ('act20mini/level_act20mini_st06_nep0num.csv', 'line-758',
     '«Порядком и Оружием»', '«Оружием и Порядком»'),
]
