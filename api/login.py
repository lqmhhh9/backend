from datetime import datetime

import psycopg2
from flask import Blueprint, jsonify, request

import config

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({
            "code": 200,
            "msg": "Please use POST to submit username and password"
        })

    data = request.get_json(silent=True) or request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            "code": 400,
            "msg": "username and password are required"
        }), 400

    exists = find(username, password)
    if exists:
        code=1
    else:
        code=0

    return jsonify({
        "code": code,
        "msg": "login success",
        "data": {
            "username": username
        }
    })


def find(username, password):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=config.PG_HOST,
            port=config.PG_PORT,
            dbname=config.PG_DATABASE,
            user=config.PG_USER,
            password=config.PG_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s LIMIT 1",
            (username, password)
        )
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"PostgreSQL error: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")
    print(year, month, day, hour, minute, second)
