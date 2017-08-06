#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017-08-05 Sydney <theodoruszq@gmail.com>

"""
"""

import torch
from torch.autograd import Variable
from torchvision import models

import cv2
import sys
import numpy as np
import argparse


class ModifiedVGG16Model(torch.nn.Module):
    def __init__(self):
        super(ModifiedVGG16Model, self).__init__()
        model = models.vgg16(pretrained = True)
        self.features = model.features  # Pretrained model divides itself to features(Map) and classifier(FC)

        for param in self.features.parameters():
            param.requires_grad = False

        # Origin classifier
        # Sequential (
        # (0): Linear (25088 -> 4096)
        # (1): ReLU (inplace)
        # (2): Dropout (p = 0.5)
        # (3): Linear (4096 -> 4096)
        # (4): ReLU (inplace)
        # (5): Dropout (p = 0.5)
        # (6): Linear (4096 -> 1000))
        self.classifier = nn.Sequential(
                nn.Dropout(),               # Default p = 0.5
                nn.Linear(25088, 4096),
                nn.ReLU(inplace = True),
                nn.Dropout(),
                nn.Linear(4096, 4096),
                nn.ReLU(inplace = True),
                nn.Linear(4096, 2))

    def forward(self, x):
        x = self.features(x)
        # https://stackoverflow.com/questions/42479902/how-view-method-works-for-tensor-in-torch
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x




def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", dest="train", action="store_true")
    parser.add_argument("--prune",  dest="prune", action="store_true")
    parser.add_argument("--train_path", type=str, default="train")
    parser.add_argument("--test_path",  type=str, default="test")
    parser.set_defaults(train=False)
    parser.set_defaults(prune=False)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    if args.train:
        model = ModifiedVGG16Model().cuda()



