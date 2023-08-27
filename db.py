# db.py
import os
import pymysql
from flask import jsonify
import random

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = f'/cloudsql/{db_connection_name}'
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user,
                                    password=db_password,
                                    unix_socket=unix_socket,
                                    db=db_name,
                                    cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        return e
    return conn


def get():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM insults;')
        insults = cursor.fetchall()
        return jsonify(insults) if result > 0 else 'No Insults in DB'


def create(insult):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO insults (insult) VALUES(%s)',
                        (insult["insult"]))
    conn.commit()
    conn.close()
    
def get_random():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM insults;')
        insults = cursor.fetchall()

        if result < 1:
            return 'No Insults in DB'
        random_insult = random.choice(insults)
        return jsonify(random_insult)
    
def delete_insult_by_id(insult_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM insults WHERE insult_id = %s', (insult_id,))
    conn.commit()
    conn.close()
