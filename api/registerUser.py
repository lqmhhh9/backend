from datetime import datetime

import psycopg2
from flask import Blueprint, jsonify, request

import config

registerUser_bp = Blueprint('registerUser', __name__)


@registerUser_bp.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
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

    status = insert_user(username, password)
    # code==1 success
    if status == "success":
        return jsonify({
            "code": 1,
            "msg": "register success",
            "data": {
                "username": username
            }
        })
    # code==-1 exist
    if status == "exists":
        return jsonify({
            "code": -1,
            "msg": "username already exists"
        })
    # code==0 failed
    return jsonify({
        "code": 0,
        "msg": "register failed"
    })


def insert_user(username, password):
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
            'SELECT 1 FROM "users" WHERE username = %s LIMIT 1',
            (username,)
        )
        if cursor.fetchone() is not None:
            return "exists"

        cursor.execute(
            'INSERT INTO "users" (username, password) VALUES (%s, %s)',
            (username, password)
        )
        conn.commit()
        return "success"
    except Exception as e:
        if conn is not None:
            conn.rollback()
        print(f"PostgreSQL error: {e}")
        return "error"
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
