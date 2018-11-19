from ctypes import *
from time import sleep
from ctypes.wintypes import POINT

user32 = windll.user32
VirtualToScan = lambda vk: user32.MapVirtualKeyA(vk, 0)
CharToVirtual = lambda c: user32.VkKeyScanW(c)
GetMessageExtraInfo = lambda: user32.GetMessageExtraInfo()

LEFTDOWN   = 0x0002
LEFTUP     = 0x0004
MIDDLEDOWN = 0x0020
MIDDLEUP   = 0x0040
RIGHTDOWN  = 0x0008
RIGHTUP    = 0x0010

MOVE       = 0x0001
ABSOLUTE   = 0x8000

XDOWN      = 0x0080
XUP        = 0x0100
WHEEL      = 0x0800
HWHEEL     = 0x01000

def mouse_pos():
    p = POINT()
    user32.GetCursorPos(byref(p))
    return (p.x, p.y)

def mouse_move(x, y):
    user32.SetCursorPos(x, y)

def mouse_event(_type, x=0, y=0, data=0):
    if _type == ABSOLUTE:
        x *= 65535
        y *= 65535
    user32.mouse_event(_type, int(x), int(y), int(data), GetMessageExtraInfo())

def mouse_click(x=-1, y=-1, duration=0.02):
    yeet = False
    if x == -1:
        x = mouse_pos()[0]
    if y == -1:
        y = mouse_pos()[1]
    if x != -1 or y != -1:
        mouse_move(x, y)
        
    mouse_event(LEFTDOWN, x=x, y=y)
    sleep(duration / 2)
    mouse_event(LEFTUP, x=x, y=y)
    sleep(duration / 2)

#1 is one wheel scroll
def mouse_scroll(amount):
    mouse_event(WHEEL, 0, 0, int(amount * 120))

def key_down(virtualCode):
    user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 0, 0)

def key_up(virtualCode):
    user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 2, 0)

def simulate_keyhit(virtualCode, duration=0.02):
    user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 0, 0)
    sleep(duration / 2);
    user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 2, 0)
    sleep(duration / 2)

def type_string(string, end="\n", interval=0.02):
    for char in string:
        b = bytes(char, 'utf-8')
        char = c_char(b)
        result = CharToVirtual(char)

        virtual = result & 0xff
        special = result & 0x00ff

        if special == 1: key_down(0x10)
        if special == 2: key_down(0x11)        
        if special == 4: key_down(0x12)
        
        simulate_keyhit(virtual, duration=interval)

        if special == 4: key_up(0x12)
        if special == 2: key_up(0x11)        
        if special == 1: key_up(0x10)
            

