import torch.nn as nn
from collections import OrderedDict

defaultcfg = [
    64,
    64,
    "M",
    128,
    128,
    "M",
    256,
    256,
    256,
    "M",
    512,
    512,
    512,
    "M",
    512,
    512,
    512,
]


class VGG(nn.Module):
    def __init__(self, compress_rate=[0.0] * 13, num_classes=10, cfg=None):
        super(VGG, self).__init__()

        if cfg is None:
            cfg = defaultcfg

        self.compress_rate = compress_rate[:]

        self.features = self._make_layers(cfg)
        last_conv_out_channels = self.features[-3].out_channels
        self.classifier = nn.Sequential(
            OrderedDict(
                [
                    ("linear1", nn.Linear(last_conv_out_channels, cfg[-1])),
                    ("norm1", nn.BatchNorm1d(cfg[-1])),
                    ("relu1", nn.ReLU(inplace=True)),
                    ("linear2", nn.Linear(cfg[-1], num_classes)),
                ]
            )
        )

    def _make_layers(self, cfg):
        layers = nn.Sequential()
        in_channels = 3
        cnt = 0

        for i, x in enumerate(cfg):
            if x == "M":
                layers.add_module("pool%d" % i, nn.MaxPool2d(kernel_size=2, stride=2))
            else:
                x = int(x * (1 - self.compress_rate[cnt]))
                cnt += 1
                conv2d = nn.Conv2d(in_channels, x, kernel_size=3, padding=1)
                layers.add_module("conv%d" % i, conv2d)
                layers.add_module("norm%d" % i, nn.BatchNorm2d(x))
                layers.add_module("relu%d" % i, nn.ReLU(inplace=True))
                in_channels = x

        return layers

    def forward(self, x):
        x = self.features(x)
        x = nn.AvgPool2d(2)(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def vgg_16_bn(compress_rate=[0.0] * 13, num_classes=10):
    return VGG(compress_rate=compress_rate, num_classes=num_classes)
