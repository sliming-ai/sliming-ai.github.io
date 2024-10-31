from typing import Optional
import torch
import torch.nn as nn
from torch import Tensor

__all__ = [
    "resnet20",
    "resnet32",
    "resnet44",
    "resnet56",
    "resnet110",
    "resnet1202",
]


def adapt_channel(compress_rate, layers):
    stage_out_channel = [16] + [16] * layers[0] + [32] * layers[1] + [64] * layers[2]
    stage_oup_cprate = []
    stage_oup_cprate += [compress_rate[0]]
    for i in range(len(layers)):
        stage_oup_cprate += [compress_rate[i + 1]] * layers[i]
    stage_oup_cprate += [0.0] * layers[-1]
    mid_cprate = compress_rate[len(layers) :]

    overall_channel = []
    mid_channel = []
    for i in range(len(stage_out_channel)):
        if i == 0:
            overall_channel += [int(stage_out_channel[i] * (1 - stage_oup_cprate[i]))]
        else:
            overall_channel += [int(stage_out_channel[i] * (1 - stage_oup_cprate[i]))]
            mid_channel += [int(stage_out_channel[i] * (1 - mid_cprate[i - 1]))]

    return overall_channel, mid_channel


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=dilation,
        groups=groups,
        bias=False,
        dilation=dilation,
    )


def conv1x1(in_planes: int, out_planes: int, stride: int = 1):
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


class BasicBlock(nn.Module):
    expansion: int = 1

    def __init__(
        self,
        midplanes,
        inplanes: int,
        planes: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
    ):
        super().__init__()
        self.conv1 = conv3x3(inplanes, midplanes, stride)
        self.bn1 = nn.BatchNorm2d(midplanes)
        self.conv2 = conv3x3(midplanes, planes)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = torch.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = torch.relu(out)

        return out


class Bottleneck(nn.Module):
    expansion: int = 4

    def __init__(
        self,
        inplanes,
        planes,
        stride,
        downsample: Optional[nn.Module] = None,
        base_width=64,
        dilation=1,
    ):
        super().__init__()
        width = int(planes * (base_width / 64.0))
        self.conv1 = conv1x1(inplanes, width)
        self.bn1 = nn.BatchNorm2d(width)
        self.conv2 = conv3x3(width, width, stride, dilation)
        self.bn2 = nn.BatchNorm2d(width)
        self.conv3 = conv1x1(width, planes * self.expansion)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):
    def __init__(
        self, block, layers, compress_rate, num_classes, width, zero_init_residual=False
    ):
        super().__init__()
        self.inplanes = width
        self.dilation = 1
        replace_stride_with_dilation = [False, False, False]

        self.overall_channel, self.mid_channel = adapt_channel(compress_rate, layers)

        self.layer_num = 0
        self.embed = nn.Sequential(
            nn.Conv2d(
                3,
                self.overall_channel[self.layer_num],
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                self.overall_channel[self.layer_num],
            ),
            nn.ReLU(inplace=True),
        )
        self.layer_num += 1

        self.layer1 = self._make_layer(block, width, layers[0], stride=1)
        self.layer2 = self._make_layer(
            block,
            width * 2,
            layers[1],
            stride=2,
            dilate=replace_stride_with_dilation[0],
        )
        self.layer3 = self._make_layer(
            block,
            width * 4,
            layers[2],
            stride=2,
            dilate=replace_stride_with_dilation[1],
        )

        last_out_channels = self.layer3[-1].conv2.out_channels
        self.layer4 = nn.Identity()
        self.fc = nn.Linear(last_out_channels * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        # Zero-initialize the last BN in each residual branch,
        # so that the residual branch starts with zeros, and each residual block behaves like an identity.
        # This improves the model by 0.2~0.3% according to https://arxiv.org/abs/1706.02677
        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck) and m.bn3.weight is not None:
                    nn.init.constant_(m.bn3.weight, 0)  # type: ignore[arg-type]
                elif isinstance(m, BasicBlock) and m.bn2.weight is not None:
                    nn.init.constant_(m.bn2.weight, 0)  # type: ignore[arg-type]

    def _make_layer(self, block, planes, blocks, stride=1, dilate=False):
        downsample = None
        if dilate:
            self.dilation *= stride
            stride = 1
        if stride != 1 or self.inplanes != self.overall_channel[self.layer_num]:
            downsample = nn.Sequential(
                conv1x1(
                    self.overall_channel[self.layer_num - 1],
                    self.overall_channel[self.layer_num],
                    stride,
                ),
                nn.BatchNorm2d(self.overall_channel[self.layer_num]),
            )

        layers = []
        layers.append(
            block(
                self.mid_channel[self.layer_num - 1],
                self.overall_channel[self.layer_num - 1],
                self.overall_channel[self.layer_num],
                stride,
                downsample,
            )
        )
        self.layer_num += 1

        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(
                block(
                    self.mid_channel[self.layer_num - 1],
                    self.overall_channel[self.layer_num - 1],
                    self.overall_channel[self.layer_num],
                    stride=1,
                )
            )
            self.layer_num += 1

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.embed(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = x.mean(-1).mean(-1)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x


def resnet20(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [3, 3, 3], compress_rate, num_classes, width)


def resnet32(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [5, 5, 5], compress_rate, num_classes, width)


def resnet44(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [7, 7, 7], compress_rate, num_classes, width)


def resnet56(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [9, 9, 9], compress_rate, num_classes, width)


def resnet110(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [18, 18, 18], compress_rate, num_classes, width)


def resnet1202(compress_rate, num_classes, width=16):
    return ResNet(BasicBlock, [200, 200, 200], compress_rate, num_classes, width)
