from time import sleep
from ctypes import *
from ctypes.wintypes import POINT
user32 = windll.user32

SCAN_F5 = 63
VK_F5 = 0x74

sleep(10)

p = POINT()
p.x = 570
p.y = 349

MOUSEEVENTF_LEFTDOWN = 0x0002

MOUSEEVENTF_LEFTUP = 0x0004

while True:
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.1)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    sleep(0.1)
    user32.keybd_event(VK_F5, SCAN_F5, 0, 0)
    sleep(0.1)
    user32.keybd_event(VK_F5, SCAN_F5, 0x0002, 0)
    sleep(8)
