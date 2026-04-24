from torch.utils.data import Dataset
import os
import cv2

from PIL import Image

class CitrusDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = ['半成熟', '成熟', '未成熟']

        self.image_paths = []
        self.labels = []

        # 遍历每个类别文件夹
        for idx, cls in enumerate(self.classes):
            cls_dir = os.path.join(root_dir, cls)
            for img_name in os.listdir(cls_dir):
                img_path = os.path.join(cls_dir, img_name)
                self.image_paths.append(img_path)
                self.labels.append(idx)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # 读取图片
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]

        # 数据增强
        if self.transform:
            image = self.transform(image)

        return image, label