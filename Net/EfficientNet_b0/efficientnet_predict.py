import torch
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
import os
from Net.EfficientNet_b0.model import EfficientNetB0


def efficientnet_predict(dic):
    # ================== 路径配置 ==================
    image_root = "E:\\xuexi\\python\\bishe\\backend\\images"
    save_root = "E:\\xuexi\\python\\bishe\\backend\\result"
    os.makedirs(save_root, exist_ok=True)

    # ================== 模型 ==================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = EfficientNetB0(num_classes=3)
    model.load_state_dict(torch.load(
        "E:\\xuexi\\python\\bishe\\backend\\Net\\EfficientNet_b0\\weights\\best_maturity.pth",
        map_location=device
    ))
    model.to(device)
    model.eval()

    class_names = ['半成熟', '成熟', '未成熟']

    # ================== 预处理 ==================
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.224, 0.224, 0.225])
    ])

    # 字体（防止中文乱码）
    try:
        font = ImageFont.truetype("simhei.ttf", 20)
    except:
        font = None

    # ================== 主流程 ==================
    for img_name, (crop_paths, boxes) in dic.items():

        # 👉 拼接原图完整路径
        original_path = os.path.join(image_root, img_name)

        if not os.path.exists(original_path):
            print(f"❌ 原图不存在: {original_path}")
            continue

        # 读取原图
        image = Image.open(original_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        orange_no=0
        orange_half=0
        orange_all=0
        for crop_path, box in zip(crop_paths, boxes):

            try:
                # 分类
                crop_img = Image.open(crop_path).convert("RGB")
                input_tensor = transform(crop_img).unsqueeze(0).to(device)

                with torch.no_grad():
                    output = model(input_tensor)
                    pred = torch.argmax(output, dim=1).item()
                    print("pred:", pred)
                    label = class_names[pred]
                    if pred == 0:
                        orange_half+=1
                    if pred == 1:
                        orange_all+=1
                    if pred == 2:
                        orange_no+=1


                xmin, ymin, xmax, ymax = box

                # 画框
                draw.rectangle([xmin, ymin, xmax, ymax],
                               outline="red", width=3)

                # 写字
                text_pos = (xmin, max(0, ymin - 20))
                draw.text(text_pos, label, fill="red", font=font)

            except Exception as e:
                print(f"❌ 处理失败: {crop_path}，原因: {e}")

        # 保存结果
        save_path = os.path.join(save_root, "result_" + img_name)
        image.save(save_path)
        print(f"✅ 已保存: {save_path}")

    return {"orange_half": orange_half,"orange_all": orange_all,"orange_no": orange_no}

if __name__ == '__main__':
    dic= {'1777272236156_root.jpg': [['E:\\xuexi\\python\\bishe\\backend\\Net\\EfficientNet_b0\\images\\0.jpg', 'E:\\xuexi\\python\\bishe\\backend\\Net\\EfficientNet_b0\\images\\1.jpg'], [(223, 167, 464, 414), (123, 356, 407, 640)]]}
    dic=efficientnet_predict(dic)
    print(dic)