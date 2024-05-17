import sqlite3
from config import *


def add_dish(test):
    if not test:
        context = config
    else:
        context = test_config

    connection = sqlite3.connect(context.db_path)
    cursor = connection.cursor()

    cursor.execute(f'''
        INSERT INTO DISHES (NAME, INGREDIENTS, RECIPE, TYPEID) 
        VALUES ('name', 'ingredients', 'recipe', (SELECT ID FROM TYPES WHERE TYPE = 'Завтрак'));
        ''')

    connection.commit()
    connection.close()


add_dish(False)
