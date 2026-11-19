# -*- coding: utf-8 -*-
"""Полная смысловая вычитка act3d0, вторая половина (RU <-> ZH <-> EN)."""
PATCHES = [
    # 03_beg — имена/канон
    ('story/act3d0/level_act3d0_03_beg_nep0num.csv', 'line-9', 'Приказ Клонина', 'Приказ Кронина'),
    ('story/act3d0/level_act3d0_03_beg_nep0num.csv', 'line-10', 'не навредите госпоже', 'не навредите мисс Цейлон'),
    ('story/act3d0/level_act3d0_03_beg_nep0num.csv', 'line-42', 'Сейлон, уходим!', 'Цейлон, уходим!'),

    # 03_end — имена/термины
    ('story/act3d0/level_act3d0_03_end_nep0num.csv', 'line-16', 'Сильванс', 'Сайленс'),
    ('story/act3d0/level_act3d0_03_end_nep0num.csv', 'line-25', 'Огнемёт на основе ориниума... И такая мощность, впечатляющий мастер искусств.', 'Огнемёт на основе Ориджиниума... И такая мощность, впечатляющий кастер.'),
    ('story/act3d0/level_act3d0_03_end_nep0num.csv', 'line-59', 'Хеллаг.', 'Хеллагур.'),

    # st02 — термин «Катастрофа» / «посланник Катастрофы», смысл
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-8', 'до возникновения полноценного бедствия', 'до Катастрофы'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-9', 'двух-четырех недель', 'двух–четырёх недель'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-51', 'к природным катаклизмам', 'к Катастрофе'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-53', 'что такой риск вообще существует', 'что Катастрофа вообще возможна'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-55', 'посланник бедствий', 'посланник Катастрофы'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-61', 'Цейлон, сможете доверить остальным?', 'Вы и остальные сможете присмотреть за Цейлон?'),
    ('story/act3d0/level_act3d0_st02_nep0num.csv', 'line-65', 'Работа посланника бедствий', 'Работа посланника Катастрофы'),

    # st03 — имя Хеллагур
    ('story/act3d0/level_act3d0_st03_nep0num.csv', 'line-169', 'дедушка Хеллаг.', 'дедушка Хеллагур.'),
    ('story/act3d0/level_act3d0_st03_nep0num.csv', 'line-173', 'Дедушка Хеллаг,', 'Дедушка Хеллагур,'),

    # st05 — имена (Шварц, Сэвидж, Скайфайр), смысл
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-17', 'сестра Бруталити', 'мисс Сэвидж'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-79', 'оставил Блэк', 'оставил Шварц'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-101', 'Блэк надеется', 'Шварц надеется'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-102', 'позволил Чёрной взять', 'позволил Шварц взять'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-106', 'цена оказалась слишком велика', 'цена оказалась почти такой же огромной'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-128', 'Чёрная тоже хотела', 'Шварц тоже хотела'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-167', 'Ой, Чёрная,', 'Ой, Шварц,'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-180', 'госпожу Эйяфьядлу и госпожу Небесный Огонь', 'мисс Эйяфьядлу и мисс Скайфайр'),
    ('story/act3d0/level_act3d0_st05_nep0num.csv', 'line-200', 'Чёрная, иди и притащи', 'Шварц, иди и притащи'),

    # ex06_end — латиница AMa-10, агирцы, регистр
    ('story/act3d0/level_act3d0_ex06_end_nep0num.csv', 'line-17', 'о вас. мисс Alty', 'о вас. Мисс Alty'),
    ('story/act3d0/level_act3d0_ex06_end_nep0num.csv', 'line-35', 'об агорцах от Frost', 'об агирцах от Frost'),
    ('story/act3d0/level_act3d0_ex06_end_nep0num.csv', 'line-147', 'АМа-10', 'AMa-10'),

    # 02_beg — имена (Шварц), термин Катастрофа, не пропустить «выводы»
    ('story/act3d0/level_act3d0_02_beg_nep0num.csv', 'line-63', 'её зовут Блэк', 'её зовут Шварц'),
    ('story/act3d0/level_act3d0_02_beg_nep0num.csv', 'line-64', 'Блэк мне как старшая сестра', 'Шварц мне как старшая сестра'),
    ('story/act3d0/level_act3d0_02_beg_nep0num.csv', 'line-100', 'Там всё подробно проанализировано.', 'Там приведены подробный анализ и выводы.'),
    ('story/act3d0/level_act3d0_02_beg_nep0num.csv', 'line-108', 'Ты вестник бедствий', 'Ты посланник Катастрофы'),

    # 08_beg — имя Скайфайр
    ('story/act3d0/level_act3d0_08_beg_nep0num.csv', 'line-29', 'Скайфаэр', 'Скайфайр'),

    # 05_beg — имена Кронин / Дойкос
    ('story/act3d0/level_act3d0_05_beg_nep0num.csv', 'line-26', 'После отказа Кронинга', 'После отказа Кронина'),
    ('story/act3d0/level_act3d0_05_beg_nep0num.csv', 'line-49', 'семьи Доркос', 'семьи Дойкос'),
    ('story/act3d0/level_act3d0_05_beg_nep0num.csv', 'line-57', 'семьи Доркос', 'семьи Дойкос'),
    ('story/act3d0/level_act3d0_05_beg_nep0num.csv', 'line-59', 'господину Кронингу', 'господину Кронину'),

    # 06_end — регистр, Метеорит, Цейлон, посланник Катастрофы
    ('story/act3d0/level_act3d0_06_end_nep0num.csv', 'line-52', 'Ориджини-слизни', 'ориджини-слизни'),
    ('story/act3d0/level_act3d0_06_end_nep0num.csv', 'line-65', 'Метеор тоже говорила', 'Метеорит тоже говорила'),
    ('story/act3d0/level_act3d0_06_end_nep0num.csv', 'line-87', 'мисс Сейлон', 'мисс Цейлон'),
    ('story/act3d0/level_act3d0_06_end_nep0num.csv', 'line-88', 'посланник по вопросам бедствий Сиесты', 'посланник Катастрофы Сиесты'),

    # 05_end — посланник Катастрофы
    ('story/act3d0/level_act3d0_05_end_nep0num.csv', 'line-25', 'Как вестник катастроф', 'Как посланник Катастрофы'),

    # 08_end — имя Скайфайр
    ('story/act3d0/level_act3d0_08_end_nep0num.csv', 'line-40', 'Скайфаер!', 'Скайфайр!'),
    ('story/act3d0/level_act3d0_08_end_nep0num.csv', 'line-116', 'Скайфаер.', 'Скайфайр.'),
]
