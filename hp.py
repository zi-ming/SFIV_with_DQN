#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/23 21:09 
'''
import numpy as np


class Hp:

    @staticmethod
    def get_hp_location(org_img):
        img = np.copy(org_img)
        h, w = img.shape[:2]
        for x in range(h):
            for y in range(w):
                b = img[x, y, 0]
                g = img[x, y, 1]
                r = img[x, y, 2]
                if x < 44:
                    img[x, y, 0] = img[x, y, 1] = img[x, y, 2] = 0
                elif r > 230 and g > 220 and b < 35:
                    img[x, y, 0] = img[x, y, 1] = img[x, y, 2] = 255
                else:
                    img[x, y, 0] = img[x, y, 1] = img[x, y, 2] = 0

        mid_w, mid_h = w // 2, h // 3
        l_lpoint_x, l_lpoint_y = 999999, 0  # 左下角的点
        l_rpoint_x, l_rpoint_y = 0, 999999  # 右上角的点

        for y in range(mid_h):
            for x in range(mid_w - 15):
                if img[y, x, 0] == 255:
                    if x <= l_lpoint_x and y >= l_lpoint_y:
                        l_lpoint_x = x
                        l_lpoint_y = y
                    if x >= l_rpoint_x and y <= l_rpoint_y:
                        l_rpoint_x = x
                        l_rpoint_y = y

        r_lpoint_x, r_lpoint_y = 999999, 999999  # 左上角的点
        r_rpoint_x, r_rpoint_y = 0, 0  # 右下角的点

        for y in range(mid_h):
            for x in range(mid_w + 15, w):
                if img[y, x, 0] == 255:
                    if x <= r_lpoint_x and y <= r_lpoint_y:
                        r_lpoint_x = x
                        r_lpoint_y = y
                    if x >= r_rpoint_x and y >= r_rpoint_y:
                        r_rpoint_x = x
                        r_rpoint_y = y

        l_lpoint_x, l_lpoint_y = l_lpoint_x + 1, l_lpoint_y - 1
        l_rpoint_x, l_rpoint_y = l_rpoint_x + 1, l_lpoint_y - 2

        r_lpoint_x, r_lpoint_y = r_lpoint_x, r_rpoint_y - 2
        r_rpoint_x, r_rpoint_y = r_rpoint_x, r_rpoint_y - 1
        # left_hp = img[l_lpoint_y:l_rpoint_y, l_lpoint_x:l_rpoint_x, :]
        # right_hp = img[r_lpoint_y:r_rpoint_y, r_lpoint_x:r_rpoint_x, :]
        # cv2.imshow('screen', left_hp)
        # cv2.waitKey(0)
        #  (h_start, h_end, w_start, w_end)
        return (l_lpoint_y - 2, l_lpoint_y - 1, l_lpoint_x - 1, l_rpoint_x + 2), \
               (r_rpoint_y - 2, r_rpoint_y - 1, r_lpoint_x - 2, r_rpoint_x + 1)

    @staticmethod
    def get_hp(img, h_start, h_end, w_start, w_end):
        hp = img[h_start:h_end, w_start:w_end, :]
        # print(hp.shape)
        # img = circle(img, w_start, h_start)
        # img = circle(img, w_end, h_end)
        # cv2.imshow('screen', img)
        # cv2.waitKey(0)
        h, w = hp.shape[:2]
        hp_amount = 0
        for y in range(h):
            for x in range(w):
                r = hp[y, x, 2]
                # print(r)
                if r > 190:
                    hp_amount += 1
        return hp_amount