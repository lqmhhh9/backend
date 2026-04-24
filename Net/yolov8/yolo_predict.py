from numpy.distutils.log import good
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
        conf=0.5,
        save_conf=True
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
    with open("runs/detect/predict/labels/image0.txt","r") as f:
        content=f.readlines()
    orange_num=len(content)
    conf_sum=0
    good=0
    bad=0
    for i in range(orange_num):
        # print("content:",content[i])
        label=content[i].split(" ")[0]
        conf=float(content[i].split(" ")[-1])
        conf_sum+=conf
        if label=="1":
            bad+=1
        else:
            good+=1
    conf_sum/=orange_num
    return{"good":good,"bad":bad,"orange_num":orange_num,"conf":conf_sum}



if __name__ == '__main__':
    # img=cv2.imread("../images/test.jpg")
    path="E:\\xuexi\\python\\bishe\\backend\\images"
    yolo_predict(path)
