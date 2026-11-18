# -*- coding: utf-8 -*-
"""Полная смысловая сверка RU <-> ZH <-> EN, act21side, файлы 01-06 (первая половина)."""
PATCHES = [
    # ---------- 01_beg: 叙拉古/Siracusa ошибочно передано как «Сицилия» ----------
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-19', 'Сицилийцы любят', 'Сиракузцы любят'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-34', 'Сицилийцы не часто', 'Сиракузцы не часто'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-49', 'сицилийские семьи', 'сиракузские семьи'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-55', 'сицилийская семья', 'сиракузская семья'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-57', 'начало на Сицилии и пустившая', 'начало в Сиракузах и пустившая'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-59', 'себя сицилийцем', 'себя сиракузцем'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-60', 'Сицилийцы отвечали ему взаимностью, всегда уважая его по-сицилийски.', 'Сиракузцы отвечали ему взаимностью, всегда уважая его по-сиракузски.'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-62', 'Сицилийцы...', 'Сиракузцы...'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-65', 'встретить сицилийцев', 'встретить сиракузцев'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-69', 'сицилийца в Колумбии', 'сиракузца в Колумбии'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-82', 'системы семей Сицилии', 'системы семей Сиракуз'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-88', 'каждый сицилиец в это верит', 'каждый сиракузец в это верит'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-107', 'обратно на Сицилию, где', 'обратно в Сиракузы, где'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-110', 'на границе Сицилии', 'на границе Сиракуз'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-117', 'все ещё жива и вернулась на землю Сицилии', 'всё ещё жива и вернулась на землю Сиракуз'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-178', 'что Сицилия изначально', 'что Сиракуза изначально'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-198', 'когда Сицилия превратилась из региона в страну, двадцать две города', 'когда Сиракуза превратилась из региона в страну, двадцать два города'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-201', '«традиции» Сицилии', '«традиции» Сиракуз'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-202', 'в нашей неизменной Сицилии', 'в нашей неизменной Сиракузе'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-206', 'вести Сицилию в будущее', 'вести Сиракузу в будущее'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-276', 'вернулись на Сицилию из Колумбии', 'вернулись в Сиракузы из Колумбии'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-282', 'значимость для Сицилии', 'значимость для Сиракуз'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-302', 'в объятия Сицилии', 'в объятия Сиракузы'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-303', 'Сицилия наконец обрела', 'Сиракуза наконец обрела'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-326', 'вернулась на Сицилию, чтобы', 'вернулась в Сиракузы, чтобы'),
    # имена / термины
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-146', 'Цеппелина Техас', 'Челлинина Техас'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-240', 'Це... мисс Техас', 'Челли... мисс Техас'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-352', 'Цеппелина Техас', 'Челлинина Техас'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-332', 'господин Валах', 'господин Валлах'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-370', 'Алиса не говорила', 'Алессия не говорила'),
    ('act21side/level_act21side_01_beg_nep0num.csv', 'line-383', 'Алиса уже долго', 'Алессия уже долго'),

    # ---------- 01_end ----------
    ('act21side/level_act21side_01_end_nep0num.csv', 'line-54', 'Экзузиа, это точно', 'Эксузай, это точно'),
    ('act21side/level_act21side_01_end_nep0num.csv', 'line-192', 'Экзузиа, давай', 'Эксузай, давай'),
    ('act21side/level_act21side_01_end_nep0num.csv', 'line-576', 'господин Валах', 'господин Валлах'),
    ('act21side/level_act21side_01_end_nep0num.csv', 'line-588', 'господин Валах', 'господин Валлах'),
    ('act21side/level_act21side_01_end_nep0num.csv', 'line-501', 'начнется', 'начнётся'),

    # ---------- 02_beg ----------
    ('act21side/level_act21side_02_beg_nep0num.csv', 'line-19', 'как ты сжимаешь кулаки, видела кровь, сочащуюся между пальцев, когда твой противник уже не мог издать ни звука.', 'как ты бьёшь кулаком, видела кровь, сочащуюся между пальцев, когда твой противник уже не мог вымолвить ни ругательства.'),
    ('act21side/level_act21side_02_beg_nep0num.csv', 'line-432', 'не придется поутру', 'не придётся поутру'),

    # ---------- 02_end ----------
    ('act21side/level_act21side_02_end_nep0num.csv', 'line-275', 'Лапланд, семь лет', 'Лаппланд, семь лет'),
    ('act21side/level_act21side_02_end_nep0num.csv', 'line-366', 'Меня зовут Катрина', 'Меня зовут Катерина'),
    ('act21side/level_act21side_02_end_nep0num.csv', 'line-379', 'Мисс Катрина', 'Мисс Катерина'),
    ('act21side/level_act21side_02_end_nep0num.csv', 'line-433', 'псевдоним Катрина', 'псевдоним Катерина'),
    ('act21side/level_act21side_02_end_nep0num.csv', 'line-493', 'сценарий придется на время', 'сценарий придётся на время'),

    # ---------- 03_beg ----------
    ('act21side/level_act21side_03_beg_nep0num.csv', 'line-18', 'Экзусия, ты же', 'Эксузай, ты же'),
    ('act21side/level_act21side_03_beg_nep0num.csv', 'line-90', 'Экзусия, что...', 'Эксузай, что...'),
    ('act21side/level_act21side_03_beg_nep0num.csv', 'line-593', 'погубило Сицилию', 'погубило сицилийцев'),
    ('act21side/level_act21side_03_beg_nep0num.csv', 'line-665', 'Челининия, я отправляю', 'Челлинина, я отправляю'),

    # ---------- 04_beg ----------
    ('act21side/level_act21side_04_beg_nep0num.csv', 'line-117', 'господин Валах', 'господин Валлах'),
    ('act21side/level_act21side_04_beg_nep0num.csv', 'line-150', 'Я, Валах, сегодня', 'Я, Валлах, сегодня'),
    ('act21side/level_act21side_04_beg_nep0num.csv', 'line-288', 'и мне придется поступать', 'и мне придётся поступать'),
    ('act21side/level_act21side_04_beg_nep0num.csv', 'line-307', 'Экзузия и Круассан', 'Эксузай и Круассан'),
    ('act21side/level_act21side_04_beg_nep0num.csv', 'line-335', 'придется ещё подождать', 'придётся ещё подождать'),

    # ---------- 04_end ----------
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-91', 'Челлинино Техас', 'Челлинина Техас'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-144', 'Ты правда удивлен, Димитри?', 'Ты правда удивлён, Дмитрий?'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-198', 'Димитри, почему?', 'Дмитрий, почему?'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-336', 'Лапленд, изгнанная', 'Лаппланд, изгнанная'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-457', 'Лапленд Салуццо', 'Лаппланд Салуццо'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-474', 'Лапленд Салуццо', 'Лаппланд Салуццо'),
    ('act21side/level_act21side_04_end_nep0num.csv', 'line-481', 'как нечто плохое', 'как запах крови'),

    # ---------- 05_beg ----------
    ('act21side/level_act21side_05_beg_nep0num.csv', 'line-77', 'Челинина Техас', 'Челлинина Техас'),
    ('act21side/level_act21side_05_beg_nep0num.csv', 'line-261', 'Я из «Пингвин Логистикс»', 'Я ищу «Пингвин Логистикс»'),
    ('act21side/level_act21side_05_beg_nep0num.csv', 'line-332', 'Эксизия, охрана', 'Эксузай, охрана'),
    ('act21side/level_act21side_05_beg_nep0num.csv', 'line-352', 'Эксизия, будешь', 'Эксузай, будешь'),

    # ---------- 05_end: «那一位» = синьора Сицилия (женский род) ----------
    ('act21side/level_act21side_05_end_nep0num.csv', 'line-169', '«того самого»', '«той самой»'),
    ('act21side/level_act21side_05_end_nep0num.csv', 'line-172', 'заставить его уйти', 'заставить её уйти'),
    ('act21side/level_act21side_05_end_nep0num.csv', 'line-201', 'что он хочет отдать управление', 'что она хочет отдать управление'),
    ('act21side/level_act21side_05_end_nep0num.csv', 'line-215', 'для него лишь забавное', 'для неё лишь забавное'),
    ('act21side/level_act21side_05_end_nep0num.csv', 'line-334', 'в этом городе, Валах', 'в этом городе, Валлах'),

    # ---------- 06_beg ----------
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-46', 'Челинина, наше первоначальное', 'Челлинина, наше первоначальное'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-50', 'клыками Зарро', 'клыками Заро'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-98', 'что Челинина тоже', 'что Челлинина тоже'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-132', 'мисс Катарины', 'мисс Катерины'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-138', 'Экзусия уже пошла', 'Эксузай уже пошла'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-142', 'сёстры Экзусии', 'сёстры Эксузай'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-183', 'мисс Катарина?!', 'мисс Катерина?!'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-188', 'Джованна и Челинина', 'Джованна и Челлинина'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-190', 'мисс Катарины?', 'мисс Катерины?'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-301', 'Валах, ты не останешься', 'Валлах, ты не останешься'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-318', 'я опаздала', 'я опоздала'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-464', 'мисс Катариной', 'мисс Катериной'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-466', 'Мисс Катарина,', 'Мисс Катерина,'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-585', 'начнется', 'начнётся'),
    ('act21side/level_act21side_06_beg_nep0num.csv', 'line-608', 'это правда ты, Челинина', 'это правда ты, Челлинина'),

    # ---------- 06_end ----------
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-158', 'сегодня Джованна должна остаться здесь навсегда.', 'сегодня Джованна должна остаться здесь.'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-176', 'Ты... Валах.', 'Ты... Валлах.'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-302', 'Экзусия, Сора в опасности', 'Эксузай, Сора в опасности'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-414', 'Челиния?', 'Челлинина?'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-507', 'Валах, в театре', 'Валлах, в театре'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-509', 'Челиния направилась', 'Челлинина направилась'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-545', 'Димитри.', 'Дмитрий.'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-557', 'Валах.', 'Валлах.'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-675', 'Челиния.', 'Челлинина.'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-792', 'Валах посмотрел', 'Валлах посмотрел'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-814', '«Челиния, какая радость', '«Челлинина, какая радость'),
    ('act21side/level_act21side_06_end_nep0num.csv', 'line-824', 'Давно не виделись, Челиния.', 'Давно не виделись, Челлинина.'),
]
