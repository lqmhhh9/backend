from Net.EfficientNet_b0.model import EfficientNetB0
from Net.yolov8.yolo_predict import yolo_predict
from api.process import process
import cv2
import config
import os
import shutil
from Net.EfficientNet_b0.efficientnet_predict import efficientnet_predict
def predict(img_path: str) -> dict:
    img=cv2.imread(img_path)
    img_name=img_path.split("/")[-1]
    print("img_name:",img_name)
    yolo_result=yolo_predict(img)
    yolo_predict_path=config.YOLO_PREDICT_PATH
    # print("process(yolo_predict_path,img_name):",yolo_predict_path,img_name)
    dic=process(yolo_predict_path,img_name)

    # print("dic:",dic)

    ENet_result=efficientnet_predict(dic)

    username=img_name.split("_")[1].split(".jpg")[0]
    # print("username:",username)

    if os.path.exists(f"./record/{username}"):
        pass
    else:
        os.mkdir(f"./record/{username}")
    src = "runs/detect/predict/image0.jpg"
    dst = os.path.join("record", username,f"yolo_result_{img_name}")
    shutil.copy(src, dst)
    src = os.path.join("result", f"result_{img_name}")
    dst = os.path.join("record", username, f"ENet_result_{img_name}")
    shutil.copy(src, dst)
    print("yolo_result:", yolo_result)
    return yolo_result,ENet_result

if __name__ == '__main__':
    predict("../images/3358dcab0017f982b93a2fd8be428a31~tplv-a9rns2rl98-pc_smart_face_crop-v1_512_384.jpg")