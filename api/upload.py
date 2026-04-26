from datetime import datetime
import os
import json
import psycopg2
from flask import Blueprint, jsonify, request
import shutil
import config
from api.predict import predict

upload_bp = Blueprint('upload', __name__)
"""
上传记录，包含批次编号、图片编号、备注信息。
"""


@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({
            'code': 0,
            'message': '没有接收到文件'
        })

    file = request.files['file']
    batch_id = request.form['batchNo']
    image_id = request.form['imageId']
    remark = request.form['remark']
    username = request.form['username']

    if file.filename == '':
        return jsonify({
            'code': 0,
            'message': '文件名为空'
        })

    save_path = f"images/{image_id}.jpg"
    file.save(save_path)

    status = insert_record(batch_id, image_id, remark, username)
    if status == "user_not_found":
        return jsonify({
            "code": 404,
            "message": "username not found"
        }), 404

    if status == "error":
        return jsonify({
            "code": 500,
            "message": "insert record failed"
        }), 500

    yolo_result=predict(save_path)
    insert_result(image_id,yolo_result)
    # shutil.rmtree("runs")
    # os.remove(f"result/result_{image_id}.jpg")
    # os.remove(f"images/{image_id}.jpg")
    return jsonify({
        "code": 200,
        "message": "upload success",
        "data": {
            "batch_id": batch_id,
            "image_id": image_id,
            "remark": remark,
            "username": username
        }
    })

def insert_result(image_id, yolo_result):
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
        print("yolo_result:",yolo_result)
        r=json.dumps(yolo_result, ensure_ascii=False)
        print("r:",r)
        cursor.execute(
            """
            INSERT INTO result (image_id, yolo_result)
            VALUES (%s, %s)
            """,
            (image_id, r)
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

def insert_record(batch_id, image_id, remark, username):
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
            return "user_not_found"

        user_id = user_row[0]
        cursor.execute(
            """
            INSERT INTO record (user_id, batch_id, image_id, remark)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, batch_id, image_id, remark)
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
