from flask import Flask, jsonify, request
import psycopg2

import hashlib
import pyotp
import random
import string
from cryptography.fernet import Fernet
import time
import base64
from bcrypt import hashpw, gensalt

app = Flask(__name__)


def encrypt_data(data, key):
    return Fernet(key).encrypt(data)


def decrypt_data(encrypted_data, key):
    return Fernet(key).decrypt(encrypted_data)


def create_totp_generators():
    conn = get_connection()
    cur = conn.cursor()

    sql = """SELECT email, secret_key, symmetric_key
             FROM users;"""
    cur.execute(sql)
    user_data = cur.fetchall()

    cur.close()
    conn.close()

    generators = {}
    for user in user_data:
        generators.update({user[0]: pyotp.TOTP(decrypt_data(user[1], user[2]))})

    return generators


def add_new_generator(login, secret_key, symmetric_key):
    generators.update({login: pyotp.TOTP(decrypt_data(secret_key, symmetric_key))})


def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )


generators = create_totp_generators()


# sql = """CREATE TABLE users (
#     id SERIAL PRIMARY KEY,
#     email VARCHAR(255),
#     password VARCHAR(255),
#     symmetric_key VARCHAR(255),
#     secret_key VARCHAR(255),
#     auth BOOLEAN
# );
# """
# cur.execute(sql)
# conn.commit()


@app.route('/register', methods=['POST'])
def reg():
    conn = get_connection()
    cur = conn.cursor()

    body = request.get_json()

    salt = gensalt()

    sql = """INSERT INTO users (email, password, symmetric_key, secret_key, auth, salt)
             VALUES (%s, %s, %s, %s, %s, %s);"""
    symmetric_key = Fernet.generate_key()
    secret_key = encrypt_data(pyotp.random_base32().encode('utf-8'), symmetric_key)
    data = (body['email'], hashpw(body['password'].encode('utf-8'), salt), symmetric_key,
            secret_key, False, salt)
    cur.execute(sql, data)

    conn.commit()
    cur.close()

    add_new_generator(body['email'], secret_key, symmetric_key)

    return 'Registered'


@app.route('/auth', methods=['POST'])
def auth():
    conn = get_connection()
    cur = conn.cursor()

    body = request.get_json()

    sql = """SELECT * FROM users WHERE email = %s;"""
    data = (body['email'],)
    cur.execute(sql, data)
    result = cur.fetchone()

    if result:
        sql = """SELECT salt FROM users WHERE email = %s AND password = %s;"""
        salt = bytes(result[6])
        data = (body['email'], hashpw(body['password'].encode('utf-8'), salt))
        cur.execute(sql, data)
        condition1 = cur.fetchone()

        cur.close()
        conn.close()

        if condition1:
            if body['totp'] == generators.get(body['email']).now():
                return 'Success auth'
            else:
                return 'Wrong TOTP'
        else:
            return 'Wrong password'
    else:
        return 'Acc not found'





app.run(port=5000)
