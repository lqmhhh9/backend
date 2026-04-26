from datetime import datetime

import psycopg2
from flask import Blueprint, jsonify, request

import config

history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        return jsonify({
            "code": 200,
            "msg": "Please use POST to submit username"
        })

    data = request.get_json(silent=True) or request.form
    username = data.get('username')

    if not username:
        return jsonify({
            "code": 400,
            "msg": "username is required"
        }), 400

    records = find_records_by_username(username)
    if records is None:
        return jsonify({
            "code": 404,
            "msg": "username not found"
        }), 404

    return jsonify({
        "code": 200,
        "msg": "history success",
        "data": records
    })


def find_records_by_username(username):
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
            'SELECT user_id FROM "users" WHERE username = %s LIMIT 1',
            (username,)
        )
        user_row = cursor.fetchone()
        if user_row is None:
            return None

        user_id = user_row[0]
        cursor.execute(
            """
            SELECT user_id, batch_id, image_id, remark
            FROM record
            WHERE user_id = %s
            ORDER BY batch_id DESC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()

        records = []
        for row in rows:
            records.append({
                "user_id": row[0],
                "batch_id": row[1],
                "images_id": row[2],
                "remark": row[3]
            })
        return records
    except Exception as e:
        print(f"PostgreSQL error: {e}")
        return []
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
