#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/23 19:43 
'''
from enum import Enum
from control_keys import control_key, ControlKeyMapping


class GameStatus(Enum):
    ROUND_OVER = 0
    READY = 1
    FIGHTING = 2
    WAITING = -1


class GameStatusChecker:
    def __init__(self, full_hp_count):
        self.last_status = GameStatus.ROUND_OVER
        self.status = GameStatus.READY
        self.waiting_count = 0
        self.ready_count = 20
        self.max_waiting_count = 150
        self.max_ready_count = 20
        self.again_count = 4000
        self.full_hp_count = full_hp_count
        self.self_win_count = 0
        self.enemy_win_count = 0

    def get_status(self, self_hp, enemy_hp):
        """获取当前游戏的状态（当前回合结束，还是新回合开始）"""
        # print(self_hp, enemy_hp, self.full_hp_count, self.status, self.ready_count, self.max_ready_count)
        if self_hp == 0 or enemy_hp == 0:
            self.waiting_count += 1
            if self.status == GameStatus.WAITING and self.waiting_count > self.max_waiting_count:
                self.status = GameStatus.ROUND_OVER
            elif self.status != GameStatus.WAITING and 10 <= self.waiting_count <= self.max_waiting_count:
                self.status = GameStatus.WAITING
        elif self_hp == enemy_hp == self.full_hp_count:
            self.ready_count += 1
            if self.status != GameStatus.FIGHTING and self.ready_count > self.max_ready_count:
                self.status = GameStatus.FIGHTING
                self.waiting_count = self.ready_count = 0

        if self.status == GameStatus.ROUND_OVER and self.waiting_count >= self.again_count:
            # time.sleep(0.5)
            control_key(ControlKeyMapping.start, delay=0.1)
            print("Will auto restart again, if it does not start for a long time, press the key `O`")

        # print(self.status, self.last_status, self_hp, enemy_hp)
        if self.status != self.last_status:
            self.last_status = self.status
            if self.status in [GameStatus.ROUND_OVER, GameStatus.FIGHTING]:
                if self.status == GameStatus.ROUND_OVER:
                    if self_hp == 0:
                        self.enemy_win_count += 1
                    if enemy_hp == 0:
                        self.self_win_count += 1
                return self.status, self.status

        return GameStatus.WAITING, self.status