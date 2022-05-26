#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Version: v1.0
@Author ：Max Lee
@Date ：2022/05/22 14:48
'''
import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api


def get_game_screen(name="SSFIVAE"):
    hwnd = win32gui.FindWindow(name, None)
    # 获取桌面
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwindc = win32gui.GetWindowDC(hwnd)

    # 创建设备描述表
    srcdc = win32ui.CreateDCFromHandle(hwindc)

    # 创建一个内存设备描述表
    memdc = srcdc.CreateCompatibleDC()

    # 创建位图对象
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, w, h)
    memdc.SelectObject(bmp)

    # 截图至内存设备描述表
    memdc.BitBlt((0, 0), (w, h), srcdc, (0, 0), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # 内存释放
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def roi(img, x, x_w, y, y_h):
    return img[y:y_h, x:x_w]


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global vertices
    if event == cv2.EVENT_LBUTTONDOWN:
        vertices.append([x, y])
    return vertices


def get_xywh(img):
    global vertices
    vertices = []

    print('Press "ESC" to quit. ')
    cv2.namedWindow("window", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("window", on_EVENT_LBUTTONDOWN)
    while True:
        cv2.imshow("window", img)
        if cv2.waitKey(0) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

    if len(vertices) != 4:
        print("vertices number not match")
        return -1

    x = min(vertices[0][0], vertices[1][0])
    x_w = max(vertices[2][0], vertices[3][0])
    y = min(vertices[1][1], vertices[2][1])
    y_h = max(vertices[0][1], vertices[3][1])

    cv2.imshow('img', img)
    cv2.imshow('roi(img)', roi(img, x, x_w, y, y_h))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f'\n x={x}, x_w={x_w}, y={y}, y_h={y_h}\n')


def circle(img, x, y):
    point_size = 2
    point_color = (0, 0, 255)
    thickness = 10
    cv2.circle(img, (x, y), point_size, point_color, thickness)
    return img


if __name__ == '__main__':
    pass
