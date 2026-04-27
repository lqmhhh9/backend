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
    print("image_id:",image_id)
    user_name=image_id.split("_")[-1].split(".")[0]

    if not image_id:
        return jsonify({
            "code": 400,
            "msg": "image_id is required"
        }), 400

    result_data = find_result_by_image_id(image_id)
    yolo_result_path=f"http://127.0.0.1:5000/api/file/record/{user_name}/yolo_result_{image_id}.jpg"
    ENet_result_path=f"http://127.0.0.1:5000/api/file/record/{user_name}/ENet_result_{image_id}.jpg"
    if result_data is None:
        return jsonify({
            "code": 404,
            "msg": "ENet_result not found"
        }), 404

    return jsonify({
        "code": 200,
        "msg": "ENet_result success",
        "data": {
            "image_id": image_id,
            "yolo_result": result_data["yolo_result"],
            "enet_result": result_data["enet_result"],
            "yolo_result_path": yolo_result_path,
            "ENet_result_path":ENet_result_path
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
            SELECT yolo_result, enet_result
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
        enet_result = row[1]

        if isinstance(yolo_result, str):
            try:
                yolo_result = json.loads(yolo_result)
            except json.JSONDecodeError:
                pass

        if isinstance(enet_result, str):
            try:
                enet_result = json.loads(enet_result)
            except json.JSONDecodeError:
                pass

        return {
            "yolo_result": yolo_result,
            "enet_result": enet_result
        }
    except Exception as e:
        print(f"PostgreSQL error: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
