import math

import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import serializers
from chainer import Variable

class VGG(chainer.Chain):
    def __init__(self, n_class=21):
        super(VGG, self).__init__(
            conv1_1=L.Convolution2D(3, 64, 3, stride=1, pad=1),
            conv1_2=L.Convolution2D(64, 64, 3, stride=1, pad=1),

            conv2_1=L.Convolution2D(64, 128, 3, stride=1, pad=1),
            conv2_2=L.Convolution2D(128, 128, 3, stride=1, pad=1),

            conv3_1=L.Convolution2D(128, 256, 3, stride=1, pad=1),
            conv3_2=L.Convolution2D(256, 256, 3, stride=1, pad=1),
            conv3_3=L.Convolution2D(256, 256, 3, stride=1, pad=1),

            conv4_1=L.Convolution2D(256, 512, 3, stride=1, pad=1),
            conv4_2=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv4_3=L.Convolution2D(512, 512, 3, stride=1, pad=1),

            conv5_1=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_2=L.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_3=L.Convolution2D(512, 512, 3, stride=1, pad=1),

            fc6=L.Linear(25088, 4096),
            fc7=L.Linear(4096, 4096),
            fc8=L.Linear(4096, n_class)
        )
        self.train = False

    def calc(self, x):
        h = F.relu(self.conv1_2(F.relu(self.conv1_1(x))))
        h = F.max_pooling_2d(h, 2, stride=2)
        h = F.relu(self.conv2_2(F.relu(self.conv2_1(h))))
        h = F.max_pooling_2d(h, 2, stride=2)
        h = F.relu(self.conv3_3(F.relu(self.conv3_2(F.relu(self.conv3_1(h))))))
        h = F.max_pooling_2d(h, 2, stride=2)
        h = F.relu(self.conv4_3(F.relu(self.conv4_2(F.relu(self.conv4_1(h))))))
        h = F.max_pooling_2d(h, 2, stride=2)
        h = F.relu(self.conv5_3(F.relu(self.conv5_2(F.relu(self.conv5_1(h))))))
        h = F.max_pooling_2d(h, 2, stride=2)
        h = F.dropout(F.relu(self.fc6(h)), train=self.train, ratio=0.5)
        h = F.dropout(F.relu(self.fc7(h)), train=self.train, ratio=0.5)
        h = self.fc8(h)
        h = F.softmax(h)
        return h

    def __call__(self, x, t=None):
        h = self.calc(x)

        if self.train:
            return F.mean_squared_error(h, t)
        else:
            return h
