# -*- coding: utf-8 -*-
""" act23side — полная построчная смысловая сверка RU <-> ZH <-> EN. """

PATCHES = [
    # --- Числа, время, меры (перевод «半/时辰» как «полгода/час») ---
    ('act23side/level_act23side_01_beg_nep0num.csv', 'line-305', 'Два часа назад', 'Четыре часа назад'),
    ('act23side/level_act23side_01_beg_nep0num.csv', 'line-345', 'Полгода назад', 'Две недели назад'),
    ('act23side/level_act23side_01_end_nep0num.csv', 'line-528', 'Полгода назад', 'Две недели назад'),
    ('act23side/level_act23side_04_end_nep0num.csv', 'line-176', 'смена каждый час', 'смена каждые два часа'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-411', 'Полгода назад', 'Час назад'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-443', 'Дважды тебе удавалось сбежать', 'Трижды тебе удавалось сбежать'),
    ('act23side/level_act23side_08_beg_nep0num.csv', 'line-104', 'закрывало большую часть неба', 'закрывало менее половины неба'),
    ('act23side/level_act23side_05_beg_nep0num.csv', 'line-225', 'на складе в пятом квартале южной части города', 'на складе на пятой улице седьмого квартала в южной части города'),
    ('act23side/level_act23side_07_end_nep0num.csv', 'line-490', 'Время уже...', 'Три четверти часа петуха...'),

    # --- Канонические имена и термины ---
    ('act23side/level_act23side_01_end_nep0num.csv', 'line-310', 'защитить Тайфу', 'защитить Тафу'),
    ('act23side/level_act23side_01_end_nep0num.csv', 'line-324', 'у господина Тайфу', 'у господина Тафу'),
    ('act23side/level_act23side_03_end_nep0num.csv', 'line-159', 'Тайфу', 'Тафу'),
    ('act23side/level_act23side_07_end_nep0num.csv', 'line-562', 'Тайфу', 'Тафу'),
    ('act23side/level_act23side_03_beg_nep0num.csv', 'line-360', 'Цзецзюнь', 'Цзеюнь'),
    ('act23side/level_act23side_06_end_nep0num.csv', 'line-95', 'Цзецзюнь', 'Цзеюнь'),
    ('act23side/level_act23side_09_beg_nep0num.csv', 'line-233', '«Чун Юэ»', '«Чунъюэ»'),
    ('act23side/level_act23side_09_beg_nep0num.csv', 'line-238', 'Чун Юэ — моё имя', 'Чунъюэ — моё имя'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-119', 'Линь Юй Ся', 'Линь Юйся'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-289', 'Линь Юй Ся', 'Линь Юйся'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-388', 'Линь Юй Ся', 'Линь Юйся'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-569', 'Линь Юй Ся', 'Линь Юйся'),
    ('act23side/level_act23side_02_beg_nep0num.csv', 'line-449', 'Крысиного короля', 'Крысиного Короля'),
    ('act23side/level_act23side_04_end_nep0num.csv', 'line-157', 'Крысиный король', 'Крысиный Король'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-23', 'Король Крыс', 'Крысиный Король'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-52', 'Дочь Короля Крыс не обязательно должна быть Королем Крыс', 'Дочь Крысиного Короля не обязательно должна быть Крысиным Королём'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-54', '«Королем Крыс»', '«Крысиным Королём»'),
    ('act23side/level_act23side_02_end_nep0num.csv', 'line-215', '«Синъюй Лоджистикс»', '«Синъюй Логистикс»'),

    # --- Ориджиниум (искажения «ориниум», «Орипатия», «Ориджини-технологии») ---
    ('act23side/level_act23side_03_beg_nep0num.csv', 'line-249', 'на ориниуме', 'на Ориджиниуме'),
    ('act23side/level_act23side_03_beg_nep0num.csv', 'line-558', 'на ориниуме', 'на Ориджиниуме'),
    ('act23side/level_act23side_08_beg_nep0num.csv', 'line-43', 'на основе ориниума', 'на основе Ориджиниума'),
    ('act23side/level_act23side_03_end_nep0num.csv', 'line-236', 'искусстве Орипатии', 'искусстве Ориджиниума'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-16', 'использовал орипатию', 'использовал искусство Ориджиниума'),
    ('act23side/level_act23side_08_end_nep0num.csv', 'line-229', 'Ориджини-технологии', 'искусства Ориджиниума'),

    # --- Го, а не шахматы (棋枰 / 纹枰 / 手谈) ---
    ('act23side/level_act23side_01_beg_nep0num.csv', 'line-516', 'с партией в шахматы', 'с партией в го'),
    ('act23side/level_act23side_09_beg_nep0num.csv', 'line-92', 'шахматную доску', 'доску для го'),
    ('act23side/level_act23side_09_beg_nep0num.csv', 'line-372', 'шахматной доски', 'доски для го'),
    ('act23side/level_act23side_st01_nep0num.csv', 'line-9', 'сыграть в шахматы', 'сыграть в го'),
    ('act23side/level_act23side_st01_nep0num.csv', 'line-10', 'шахматных премудростей', 'премудростей го'),
    ('act23side/level_act23side_st01_nep0num.csv', 'line-15', 'играть в шахматы', 'играть в го'),
    ('act23side/level_act23side_st01_nep0num.csv', 'line-16', 'Шахматные баталии', 'Партии в го'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-308', 'шахматную лавку', 'лавку для игры в го'),

    # --- Смысл, логика, лицо/род, пропущенные фразы ---
    ('act23side/level_act23side_03_beg_nep0num.csv', 'line-54', 'гроссмейстеры ещё живы', 'гроссмейстер ещё жив'),
    ('act23side/level_act23side_04_beg_nep0num.csv', 'line-214', 'даже если вас отпустить...', 'даже если вас отпустить, пользы от этого не будет...'),
    ('act23side/level_act23side_04_beg_nep0num.csv', 'line-430', 'Вы все разнесли, убирайтесь вон!', 'Вы всё здесь разнесли! Если хотите драться, выходите наружу!'),
    ('act23side/level_act23side_04_end_nep0num.csv', 'line-324', 'В её поле зрения', 'В его поле зрения'),
    ('act23side/level_act23side_01_beg_nep0num.csv', 'line-814', 'длинный нож', 'длинный клинок'),
    ('act23side/level_act23side_07_beg_nep0num.csv', 'line-534', 'длинный нож', 'длинный клинок'),
    ('act23side/level_act23side_st02_nep0num.csv', 'line-64', 'как дитя поколения офицеров или Цзо Лэ', 'как дитя одного поколения с летописцем и Цзо Лэ'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-283', 'твоя сестра', 'моя сестра'),
    ('act23side/level_act23side_st03_nep0num.csv', 'line-289', 'где в прошлом году была Си', 'где в прошлом году побывали Ниан и Даск'),

    # --- Пустая ячейка (перевод подменён плейсхолдером) ---
    ('act23side/level_act23side_st01_nep0num.csv', 'line-110', '???', 'Дайте дорогу.'),
]
