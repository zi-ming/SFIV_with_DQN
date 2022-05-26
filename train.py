#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/22 14:48
'''
import datetime
from collections import deque
from brain import Brain
from reward import Reward
from control_keys import key_check
from hp import Hp
from grab_screen import roi, get_game_screen
from game_status_checker import GameStatusChecker, GameStatus


class Player:
    def __init__(self, model_save_path=r"sf.pth"):
        self.screens = deque(maxlen=2)
        self.brain = Brain(model_save_path)
        self.reward = Reward()
        self.i = 1
        self.round_counter = 0

    def play(self):
        self.screens.append(get_game_screen())
        curr_self_hp = Hp.get_hp(self.screens[0], *self.self_location)
        curr_enemy_hp = Hp.get_hp(self.screens[0], *self.enemy_location)
        abservation = roi(self.screens[0], x=30, x_w=620, y=166, y_h=392)

        confirm, status = self.game_status_checker.get_status(curr_self_hp, curr_enemy_hp)
        if confirm == GameStatus.ROUND_OVER:    # 当前回合结束
            print("Round over...")
            return
        elif confirm == GameStatus.FIGHTING:    # 新回合开始
            self.round_counter += 1
            self.screens.clear()
            self.screens.append(get_game_screen())
            print("Start new round ...")
        elif status != GameStatus.FIGHTING:     # 等待开始新回合
            return

        action_index, action = self.brain.predict_action(abservation)
        self.screens.append(get_game_screen())
        next_self_hp = Hp.get_hp(self.screens[-1], *self.self_location)
        next_enemy_hp = Hp.get_hp(self.screens[-1], *self.enemy_location)
        next_abservation = roi(self.screens[-1], x=30, x_w=600, y=166, y_h=392)
        reward = self.reward.get_reward(action, [curr_self_hp, curr_enemy_hp],
                                        [next_self_hp, next_enemy_hp])
        if reward != 0:
            print("[{}][{}]".format(self.round_counter, reward),
                  action, curr_self_hp, curr_enemy_hp)
        self.brain.replay_memory.store(abservation, action_index, reward, next_abservation)
        if self.i % self.brain.update_freq == 0:
            self.brain.learn()
        if self.i % self.brain.target_network_update_freq == 0:
            self.brain.update_target_network()
        if self.i % self.brain.save_model_freq == 0:
            self.brain.save_evaluate_network()
            self.reward.save_reward_curve(self.round_counter)
        self.i += 1

    def run(self):
        paused = True
        print("Waiting start")
        while True:
            keys = key_check()
            if paused:
                if 'num0' in keys:
                    self.screens.append(get_game_screen())
                    # self.self_location, self.enemy_location = Hp.get_hp_location(self.screens[0])
                    self.self_location, self.enemy_location = (93, 94, 71, 289), (93, 94, 357, 575)
                    print(self.self_location, self.enemy_location)
                    curr_self_hp = Hp.get_hp(self.screens[0], *self.self_location)
                    curr_enemy_hp = Hp.get_hp(self.screens[0], *self.enemy_location)
                    print(curr_self_hp, curr_enemy_hp)
                    self.game_status_checker = GameStatusChecker(curr_self_hp)
                    paused = False
            else:
                self.play()
                if 'space' in keys:
                    self.brain.save_evaluate_network()
                    print("Saving network")
                    return


if __name__ == '__main__':
    player = Player()
    player.run()