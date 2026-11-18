# -*- coding: utf-8 -*-
"""act38side, nep0num, первая половина (01_beg .. 06_end).

Полная построчная смысловая сверка RU <-> ZH <-> EN: 12 CSV, 2313 реплик.
Правки только в 5-й колонке (Translation).
"""
PATCHES = [
    # --- 01: род/число (ZH 她, EN she/her) ---
    ('act38side/level_act38side_01_beg_nep0num.csv', 'line-142',
     'Его тоже нет, с самого вчерашнего вечера его не видно',
     'Её тоже нет, с самого вчерашнего вечера её не видно'),
    # --- 01: канонические имена оперативников (glossary.json) ---
    ('act38side/level_act38side_01_end_nep0num.csv', 'line-328',
     'Кроссант и Байзон затеяли какой-то новый международный проект, турне по Сиракузам только наполовину пройдено, а Эксизия',
     'Круассан и Байзон затеяли какой-то новый международный проект, турне по Сиракузам только наполовину пройдено, а Эксузай'),

    # --- 02: каноническое имя Lappland -> Лаппланд ---
    ('act38side/level_act38side_02_beg_nep0num.csv', 'line-331',
     'Лаплэнд', 'Лаппланд'),

    # --- 03: подмена места: 叙拉古/Siracusa -> Сиракузы (не Сицилия) ---
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-31',
     'сицилийцы', 'сиракузцы'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-270',
     '*Сицилийское ругательство*', '*Сиракузское ругательство*'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-289',
     'в Сицилию', 'в Сиракузы'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-315',
     'в Сицилию', 'в Сиракузы'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-327',
     'в Сицилию', 'в Сиракузы'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-346',
     'Вернувшись в Сицилию', 'Вернувшись в Сиракузы'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-727',
     'В Сицилии', 'В Сиракузах'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-778',
     'Сицилия действительно', 'Сиракузы действительно'),
    # --- 03: каноническое имя Lunacub -> Лунакаб ---
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-631',
     'Цзы Юэ', 'Лунакаб'),
    ('act38side/level_act38side_03_beg_nep0num.csv', 'line-672',
     'Цзы Юэ', 'Лунакаб'),

    # --- 04: канонические имена оперативников (operator_names_map.json) ---
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-95',
     'оператор Сяе', 'оператор Виджил'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-97',
     'оператора Сяе', 'оператора Виджил'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-98',
     'к госпоже Инквизиции', 'к мисс Пенанс'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-121',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-136',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-266',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-271',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-288',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-306',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-393',
     'Цзыюэ', 'Лунакаб'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-615',
     'Лапленд Салуццо', 'Лаппланд Салуццо'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-663',
     'Лапленд?', 'Лаппланд?'),
    # --- 04: род: Ingrid — женщина (ZH叙拉古人, EN Siracusan) ---
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-495',
     'была самым настоящим сиракузцем', 'была самой настоящей сиракузкой'),
    ('act38side/level_act38side_04_beg_nep0num.csv', 'line-548',
     'Ты стал настоящим сиракузцем', 'Ты стала настоящей сиракузкой'),
    # --- 04: перевёрнутая логика (ZH 也拿衰老没什么办法 / EN age has affected) ---
    ('act38side/level_act38side_04_end_nep0num.csv', 'line-38',
     'даже перед тем, кого выбрал Вагу, старость бессильна',
     'даже тот, кого выбрал Вагу, не может ничего поделать со старостью'),
    # --- 04: перевёрнутая логика (ZH 没有过去那般有耐心 / EN lack patience of youth) ---
    ('act38side/level_act38side_04_end_nep0num.csv', 'line-213',
     'ты стал нетерпелив, как и в былые годы',
     'ты стал нетерпеливее, чем в былые годы'),

    # --- 05: опечатки/орфография, канон «Инфицированные», «Катастрофа» ---
    ('act38side/level_act38side_05_beg_nep0num.csv', 'line-510',
     'Бездомная инфицировання', 'Бездомная инфицированная'),
    ('act38side/level_act38side_05_end_nep0num.csv', 'line-9',
     'и все твердила', 'и всё твердила'),
    ('act38side/level_act38side_05_end_nep0num.csv', 'line-14',
     'Она инфицировання', 'Она инфицированная'),
    ('act38side/level_act38side_05_end_nep0num.csv', 'line-376',
     'от природного бедствия', 'от Катастрофы'),
    ('act38side/level_act38side_05_end_nep0num.csv', 'line-429',
     'Но ты — инфицировання', 'Но ты — инфицированная'),

    # --- 06: опечатки «Ориджиниум», «Урсус», канон «Катастрофа» ---
    ('act38side/level_act38side_06_beg_nep0num.csv', 'line-28',
     'двигатели на ориниуме', 'двигатели на ориджиниуме'),
    ('act38side/level_act38side_06_beg_nep0num.csv', 'line-140',
     'магия ориниума', 'магия ориджиниума'),
    ('act38side/level_act38side_06_end_nep0num.csv', 'line-170',
     'охваченному бедствием Чернобогу', 'охваченному Катастрофой Чернобогу'),
    ('act38side/level_act38side_06_end_nep0num.csv', 'line-243',
     'движки на ориниуме', 'движки на ориджиниуме'),
    ('act38side/level_act38side_06_end_nep0num.csv', 'line-255',
     'взрывчатка на ориниуме', 'взрывчатка на ориджиниуме'),
    ('act38side/level_act38side_06_end_nep0num.csv', 'line-259',
     '*Урсовское ругательство*', '*Урсусское ругательство*'),
    ('act38side/level_act38side_06_end_nep0num.csv', 'line-292',
     '*Урсовское ругательство*', '*Урсусское ругательство*'),
]
