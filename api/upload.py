from api.predict import predict
from flask import Blueprint, jsonify, request
import base64
import re
from datetime import datetime

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    返回指定年级册次下的单元、课文和每课词数。
    """
    payload = request.data
    # print(payload)
    payload =str(payload)
    payload=payload[35:]
    # print(payload)
    paylaod=payload[:-3]
    # print(paylaod)
    # print(type(payload))
    img_bytes = base64.b64decode(paylaod)
    # print(img_bytes)
    now = datetime.now()
    year=now.strftime("%Y")
    month=now.strftime("%m")
    day=now.strftime("%d")
    hour=now.strftime("%H")
    minute=now.strftime("%M")
    second=now.strftime("%S")
    print(year,month,day,hour,minute,second)
    with open(f"images/{year}_{month}_{day}_{hour}_{minute}_{second}.jpg", "wb") as f:
        f.write(img_bytes)

    predict(f"images/{year}_{month}_{day}_{hour}_{minute}_{second}.jpg")
    return jsonify({
        "code": 200,
        "data": [{"user":1,"passwd":"123456"}]
    })


if __name__ == '__main__':
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")
    print(year, month, day, hour, minute, second)