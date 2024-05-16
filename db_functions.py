import sqlite3
from config import *

def get_types(test=False):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT ID, TYPE FROM TYPES
    ''')

    types = []
    for i in cursor.fetchall():
        dict_ = {
            'id': i[0],
            'type': i[1]
        }
        types.append(dict_)
    connection.close()

    return types
