import torch
import torch.nn as nn

# 核心模块：MBConv
class MBConv(nn.Module):
    def __init__(self, in_ch, out_ch, kernel_size, stride, expand_ratio):
        super().__init__()
        hidden_ch = in_ch * expand_ratio
        self.use_residual = stride == 1 and in_ch == out_ch

        layers = []
        if expand_ratio != 1:
            layers.append(nn.Conv2d(in_ch, hidden_ch, 1, bias=False))
            layers.append(nn.BatchNorm2d(hidden_ch))
            layers.append(nn.SiLU())

        layers.extend([
            nn.Conv2d(hidden_ch, hidden_ch, kernel_size, stride, kernel_size//2, groups=hidden_ch, bias=False),
            nn.BatchNorm2d(hidden_ch),
            nn.SiLU(),
            nn.Conv2d(hidden_ch, out_ch, 1, bias=False),
            nn.BatchNorm2d(out_ch)
        ])
        self.block = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_residual:
            return x + self.block(x)
        else:
            return self.block(x)

#  EfficientNet-B0
class EfficientNetB0(nn.Module):
    def __init__(self, num_classes=3):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, 3, 2, 1, bias=False),
            nn.BatchNorm2d(32),
            nn.SiLU()
        )

        self.blocks = nn.Sequential(
            MBConv(32, 16, 3, 1, 1),
            MBConv(16, 24, 3, 2, 6),
            MBConv(24, 24, 3, 1, 6),
            MBConv(24, 40, 5, 2, 6),
            MBConv(40, 40, 5, 1, 6),
            MBConv(40, 80, 3, 2, 6),
            MBConv(80, 80, 3, 1, 6),
            MBConv(80, 80, 3, 1, 6),
            MBConv(80, 112, 5, 1, 6),
            MBConv(112, 112, 5, 1, 6),
            MBConv(112, 192, 5, 2, 6),
            MBConv(192, 192, 5, 1, 6),
            MBConv(192, 192, 5, 1, 6),
            MBConv(192, 320, 3, 1, 6),
        )

        self.head = nn.Sequential(
            nn.Conv2d(320, 1280, 1, bias=False),
            nn.BatchNorm2d(1280),
            nn.SiLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(1280, num_classes)
        )

    def forward(self, x):
        x = self.stem(x)
        x = self.blocks(x)
        x = self.head(x)
        return x