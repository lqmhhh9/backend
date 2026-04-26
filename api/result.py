from datetime import datetime
import json

import psycopg2
from flask import Blueprint, jsonify, request

import config

result_bp = Blueprint('result', __name__)


@result_bp.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return jsonify({
            "code": 200,
            "msg": "Please use POST to submit image_id"
        })

    data = request.get_json(silent=True) or request.form
    image_id = data.get("image_id")

    if not image_id:
        return jsonify({
            "code": 400,
            "msg": "image_id is required"
        }), 400

    yolo_result = find_result_by_image_id(image_id)
    if yolo_result is None:
        return jsonify({
            "code": 404,
            "msg": "result not found"
        }), 404

    return jsonify({
        "code": 200,
        "msg": "result success",
        "data": {
            "image_id": image_id,
            "yolo_result": yolo_result
        }
    })


def find_result_by_image_id(image_id):
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
            """
            SELECT yolo_result
            FROM result
            WHERE image_id = %s
            LIMIT 1
            """,
            (image_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None

        yolo_result = row[0]
        if isinstance(yolo_result, str):
            try:
                return json.loads(yolo_result)
            except json.JSONDecodeError:
                return yolo_result
        return yolo_result
    except Exception as e:
        print(f"PostgreSQL error: {e}")
        return None
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
