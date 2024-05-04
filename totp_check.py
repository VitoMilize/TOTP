import argparse
import time

import psycopg2
import pyotp
from cryptography.fernet import Fernet


def encrypt_data(data, key):
    return Fernet(key).encrypt(data)


def decrypt_data(encrypted_data, key):
    return Fernet(key).decrypt(encrypted_data)


def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('get')
    parser.add_argument('--login')

    args = parser.parse_args()

    if args.get and args.login:
        conn = get_connection()
        cur = conn.cursor()

        sql = """SELECT secret_key, symmetric_key FROM users WHERE email = %s;"""
        answer = args.login
        cur.execute(sql, (answer,))

        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            secret_key_bytes = bytes(result[0])
            symmetric_key_bytes = bytes(result[1])

            generator = pyotp.TOTP(decrypt_data(secret_key_bytes, symmetric_key_bytes))
            remaining_time = generator.interval - (
                    int(time.time()) % generator.interval)
            print({
                'totp': generator.now(),
                'remaining_time': remaining_time
            })
    else:
        print('Login not found')
