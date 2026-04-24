from Net.yolov8.yolo_predict import yolo_predict
from api.process import process
import cv2
import config
from Net.EfficientNet_b0.efficientnet_predict import efficientnet_predict
def predict(img_path: str) -> str:
    img=cv2.imread(img_path)
    img_name=img_path.split("/")[-1]
    # print(img_name)
    yolo_predict(img)
    yolo_predict_path=config.YOLO_PREDICT_PATH
    print("process(yolo_predict_path,img_name):",yolo_predict_path,img_name)
    dic=process(yolo_predict_path,img_name)
    efficientnet_predict(dic)

    return ""

if __name__ == '__main__':
    predict("../images/3358dcab0017f982b93a2fd8be428a31~tplv-a9rns2rl98-pc_smart_face_crop-v1_512_384.jpg")