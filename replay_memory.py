#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/23 20:30 
'''
import torch
import random
from collections import deque


class ReplayMemory:
    def __init__(self, capacity=2000, use_cuda=True):
        self.memory = deque(maxlen=capacity)
        self.index = 0
        self.count = 0
        self.use_cuda = use_cuda
        self.capacity = capacity

    def store(self, *args):
        # 这里没有把bgr转成rgb
        observation = torch.FloatTensor(args[0]).unsqueeze(0).permute(0, 3, 1, 2)
        actions = torch.LongTensor([args[1]]).unsqueeze(0)
        rewards = torch.FloatTensor([args[2]]).unsqueeze(0)
        next_observation = torch.FloatTensor(args[-1]).unsqueeze(0).permute(0, 3, 1, 2)

        self.memory.append([observation, actions, rewards, next_observation])
        self.index += 1
        self.count = min(self.index, self.capacity)

    def sample(self, size):
        items = random.sample(self.memory, min(self.count, size))
        rets = [x.clone() for x in items[0]]
        for x in items[1:]:
            for i in range(len(rets)):
                rets[i] = torch.cat([rets[i].clone(), x[i]])
        if self.use_cuda:
            return [x.cuda() for x in rets]
        return rets

    def reset(self):
        self.i = self.count = 0
        print("Cleaning DQNReplayer...")