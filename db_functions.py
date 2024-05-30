# -*- coding: utf-8 -*-

import sqlite3
from config import *


def make_dict_list(values, keys):
    if not all(len(x) == len(keys) for x in values):
        raise Exception
    list_ = []
    for i in values:
        dict_ = dict()
        for n, j in enumerate(keys):
            dict_[j] = i[n]
        list_.append(dict_)
    return list_


def get_types(test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT ID, TYPE FROM TYPES
    ''')

    types = make_dict_list(cursor.fetchall(), ('id', 'type'))

    connection.close()

    return types


def get_admins(test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT ID, ADMIN FROM ADMINS
        ''')

    admins = [i['admin'] for i in make_dict_list(cursor.fetchall(), ('id', 'admin'))]
    connection.close()

    return {
        'core_admins': context.core_admins,
        'sub_admins': admins,
        'all_admins': admins + context.core_admins
        }


def get_dish_by_id(id_, test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute(f'''
    SELECT * FROM DISHES WHERE ID = {id_}
    ''')

    types = make_dict_list(cursor.fetchall(), ('id', 'type_id', 'name', 'ingredients', 'recipe', 'photo_id', 'add_by'))

    connection.close()

    return types[0]


def get_dish_name_by_type(type_id, test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute(f'''
    SELECT * FROM DISHES WHERE TYPEID = {type_id}
    ''')

    types = make_dict_list(cursor.fetchall(), ('id', 'type_id', 'name', 'ingredients', 'recipe', 'photo_id', 'add_by'))

    connection.close()

    return types


def add_dish(dish, test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()



    cursor.execute(f'''
            INSERT INTO DISHES (NAME, INGREDIENTS, RECIPE, PHOTOID, ADDBY, TYPEID) 
            VALUES ('{dish['name']}', '{dish['ingredients']}', '{dish['recipe']}', 
            '{dish['photo_id']}', '{dish['add_by']}', '{dish["type_id"]}');
            ''')

    connection.commit()
    connection.close()


def add_new_admin(admin, test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute(f'''
                INSERT INTO ADMINS (ADMIN) 
                VALUES ('{admin}');
                ''')
    connection.commit()
    connection.close()
