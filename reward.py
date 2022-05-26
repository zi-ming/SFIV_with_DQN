#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/22 14:48
'''
import numpy as np
import matplotlib.pyplot as plt
from control_keys import GameKeyMapping


class Reward:
    def __init__(self):
        self.total_reward = 0
        self.reward_history = []

    def get_reward(self, action, curr_hps, next_hps, weights=None):
        """
        :param curr_status: [self_hp, enemy_hp]
        :param next_status: [self_hp, enemy_hp]
        """
        if weights is None:
            weights = [1, 1]
        self_reward = next_hps[0] - curr_hps[0]
        enemy_reward = curr_hps[1] - next_hps[1]
        reward = weights[0] * self_reward + weights[1] * enemy_reward
        if abs(reward) > 18:
            reward = 0
        if action == GameKeyMapping.up and reward > 0:
            reward = 0
        self.total_reward += reward
        self.reward_history.append(self.total_reward)
        return reward

    def reset_reward(self):
        self.total_reward = 0
        self.reward_history = []

    def save_reward_curve(self, round):
        total = len(self.reward_history)
        if total > 100:
            plt.rcParams['figure.figsize'] = 100, 15
            plt.plot(np.arange(total), self.reward_history)
            plt.ylabel('reward')
            plt.xlabel('training steps')
            plt.xticks(np.arange(0, total, int(total/100)))
            plt.savefig('rewards/reward_{}.png'.format(round))
            # plt.show()