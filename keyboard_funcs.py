import ctypes as c
from ctypes.wintypes import BYTE

user32 = c.windll.user32
kernel32 = c.windll.kernel32

_keyBoardState = c.ARRAY(BYTE, 256)()

VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12

def ParseKeyboardVals():
    pass

def ToAscii(virtKey, scanCode, flags):
    buff = c.create_unicode_buffer(3)
    user32.GetKeyboardState(_keyBoardState)
    user32.ToUnicodeEx(virtKey, scanCode, _keyBoardState, buff, 3, flags, GetKeyboardLayout(0))
    return buff.value

def GetKeyState(virtkey):
    return user32.GetKeyState(virtkey)

def GetKeyboardLayout(threadId):
    return user32.GetKeyboardLayout(threadId)
