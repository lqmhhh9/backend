import os

import cv2
# "../runs/detect/predict"
def process(path:str,img_name:str)->str:
    label_path=path+"/labels/"+os.listdir(path+"/labels")[0]
    with open(label_path,'r') as f:
        content=f.readlines()
    img=cv2.imread(path+"/bak/"+img_name)
    img_h, img_w = img.shape[:2]

    index=0
    dic={}
    lst=[[],[]]
    for line in content:
        line=line.strip().split(" ")[1:]
        print(line)
        cx=float(line[0])
        cy=float(line[1])
        w=float(line[2])
        h=float(line[3])
        xmin = round(img_w * (cx - w / 2.0))
        xmax = round(img_w * (cx + w / 2.0))
        ymin = round(img_h * (cy - h / 2.0))
        ymax = round(img_h * (cy + h / 2.0))
        print(xmin, ymin, xmax, ymax)
        crop = img[ymin:ymax, xmin:xmax]
        cv2.imwrite("E:\\xuexi\\python\\bishe\\backend\\Net\\EfficientNet_b0\\images\\"+str(index)+".jpg",crop)
        # 二位列表,0维度代表裁剪图片,一维代表坐标,一维数据类型为元组
        lst[0].append("E:\\xuexi\\python\\bishe\\backend\\Net\\EfficientNet_b0\\images\\"+str(index)+".jpg")
        index += 1
        tp=(xmin, ymin, xmax, ymax)
        lst[1].append(tp)
    dic[img_name]=lst
    print(dic)
    return dic

if __name__ == '__main__':
    process("../Net/yolov8/runs/detect/predict","3358dcab0017f982b93a2fd8be428a31~tplv-a9rns2rl98-pc_smart_face_crop-v1_512_384.jpg")