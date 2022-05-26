#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/22 14:48
'''
import os
import random
import torch
import threading
import functools
import numpy as np
import torch.nn as nn
from replay_memory import ReplayMemory
from control_keys import control_key, GameKeyMapping
from torchvision.models.mobilenetv3 import mobilenet_v3_small


class Brain:
    def __init__(self, model_save_path, action_count=12, use_cuda=True):
        self.model_save_path = model_save_path
        self.use_cuda = use_cuda

        self.action_count = action_count  # 动作数量
        self.lr = 0.001  # 学习率
        self.gamma = 0.9  # 奖励衰减
        self.batch_size = 15  # 样本抽取数量
        self.update_freq = 200  # 训练评估网络的频率
        self.save_model_freq = 10000
        self.target_network_update_freq = 500  # 更新目标网络的频率
        self.random_num = 0.2
        self.min_random_num = 0.2

        self.policy_net = self.build_network()  # 评估网络
        self.target_net = self.build_network()  # 目标网络
        self.replay_memory = ReplayMemory(use_cuda=use_cuda)  # 经验回放
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=self.lr)
        self.policy_net.eval()
        self.target_net.eval()

        self.loss_func = nn.MSELoss()
        self.actions = [functools.partial(control_key, key=k) for k in GameKeyMapping]

    def build_network(self):
        model = mobilenet_v3_small(num_classes=self.action_count)
        if self.model_save_path and os.path.exists(self.model_save_path):
            self.random_num = self.min_random_num
            state_dict = torch.load(self.model_save_path)
            model.load_state_dict(state_dict)
            print("Loading " + self.model_save_path)
        if self.use_cuda:
            return model.cuda()
        return model

    def predict_action(self, abservation):
        if np.random.rand() < self.random_num:
            qs = torch.rand(self.action_count)
        else:
            with torch.no_grad():
                x = torch.unsqueeze(torch.from_numpy(abservation).float(), 0)   # 把三维的numpy转成四维 的tensor
                x = x.permute(0, 3, 1, 2)                                       # (h, w, h, c) to (h, c, w, h)
                if self.use_cuda:
                    x = x.cuda()
                qs = self.policy_net(x)

        if self.random_num > self.min_random_num:
            print("random num:", self.random_num)
            self.random_num = max(self.random_num - 0.00005, 0.2)

        action_index = torch.argmax(qs).data
        act = self.actions[action_index]
        # act()
        self.act_process = threading.Thread(target=act)
        self.act_process.start()
        return action_index, list(GameKeyMapping)[action_index]

    def learn(self):
        observations, actions, rewards, next_observations = self.replay_memory.sample(self.batch_size)

        self.policy_net.train()
        q_eval = self.policy_net(observations).gather(1, actions).squeeze()
        q_next = self.target_net(next_observations).detach().squeeze()
        q_next = q_next.max(1)[0].squeeze()
        q_target = rewards.squeeze() + self.gamma * q_next
        loss = self.loss_func(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.policy_net.eval()
        print("Updating policy network ...")

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())
        print("Updating target network ...")

    def save_evaluate_network(self):
        torch.save(self.policy_net.state_dict(), self.model_save_path)


def test():
    brain = Brain(r"sp_test.pth", use_cuda=False)
    for i in range(20):
        status_screen = np.random.randn(226, 570, 3)
        next_screen = np.random.randn(226, 570, 3)

        action = brain.predict_action(status_screen)
        brain.replay_memory.store(status_screen, action,
                                  random.randint(-20, 20),
                                  next_screen)

        # print(action)
        # if i % 10 == 0:
        #     brain.learn()
        # if i % 20 == 0:
        #     brain.update_target_network()
    # brain.save_evaluate_network()
    # print(brain.replayer.count)
    brain.learn()
    o, a, r, n = brain.replay_memory.sample(2)
    print(o.shape, a.shape, r.shape, n.shape)



if __name__ == "__main__":
    test()
    # a = np.asarray([[
    #     [1, 2, 3],
    #     [1, 2, 3],
    # ]])
    # a = a[:,:,::-1]
    # print(a)
