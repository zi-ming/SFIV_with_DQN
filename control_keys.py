import ctypes
import time
from enum import Enum
import win32api as wapi

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]



class GameKeyMapping(Enum):
    light_bunch = 0x0A        # 轻拳（9）
    medium_punch = 0x0B       # 中拳（0）
    heavy_punch = 0x0C        # 重拳（-）
    # all_punch = 0x0D          # 轻 + 中 + 重拳（=）

    light_foot = 0x18  # 轻脚（O）
    medium_foot = 0x19  # 中脚（P）
    heavy_foot = 0x1A  # 重脚（[）
    # all_foot = 0x1B  # 轻 + 中 + 重脚（]）

    wrestling = 0x26  # 摔（L）

    defense = 0x27    # 御身一击（;）
    # red_defense = 0x2B    # 红色御身一击（\）

    up = 0x48
    left = 0x4B
    right = 0x4D
    down = 0x50


class ControlKeyMapping(Enum):
    space = 0x20
    num0 = 0x60
    start = 0x18


def press_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def control_key(key, delay=0.2):
    press_key(key.value)
    time.sleep(delay)
    release_key(key.value)


def key_check():
    keys = []
    for key in ['num0', 'space']:    # 需要判断的按键就是这里
        if wapi.GetAsyncKeyState(ControlKeyMapping[key].value):    # wapi.GetAsyncKeyState() ，相应的按键正在被按着，就返回 True, 否则就返回 False
            keys.append(key)
    return keys


if __name__ == '__main__':
    control_key(GameKeyMapping.up)