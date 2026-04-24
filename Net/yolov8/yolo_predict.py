from ultralytics import YOLO

import os

import cv2

import config


def yolo_predict(path):
    weight_path=config.YOLO_MODEL
    model=YOLO(weight_path)
    results = model.predict(
        source=path,  # 图片/文件夹
        save=True,  # 保存画框图
        save_txt=True,  # 保存标签txt
        conf=0.5
    )
    path="E:\\xuexi\\python\\bishe\\backend\\Net\\yolov8\\runs\\detect\\predict"
    img_list=os.listdir("E:\\xuexi\\python\\bishe\\backend\\images")

    if os.path.exists('E:\\xuexi\\python\\bishe\\backend\\runs\\detect\\predict\\bak'):
        pass
    else:
        os.mkdir('E:\\xuexi\\python\\bishe\\backend\\runs\\detect\\predict\\bak')
    for i in img_list:
        img=cv2.imread("E:\\xuexi\\python\\bishe\\backend\\images\\"+i)
        img_path=os.path.join("E:\\xuexi\\python\\bishe\\backend\\runs\\detect\\predict\\bak",i)
        cv2.imwrite(img_path,img)




if __name__ == '__main__':
    # img=cv2.imread("../images/test.jpg")
    path="E:\\xuexi\\python\\bishe\\backend\\images"
    yolo_predict(path)
