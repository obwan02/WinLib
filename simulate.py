from ctypes import *
from time import sleep
from winlib.defs import *

user32 = windll.user32
#load = user32.LoadKeyboardLayoutA(0x00000409, 0x00000001)

VirtualToScan = lambda vk: user32.MapVirtualKeyA(vk, 0)
GetMessageExtraInfo = lambda: user32.GetMessageExtraInfo()
CharToVk = lambda char: user32.VkKeyScanA(char)

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


def mouse_move(x, y):
	user32.SetCursorPos(x, y)

def mouse_event(_type, x=0, y=0, data=0):
	if _type == ABSOLUTE:
		x *= 65535
		y *= 65535
	user32.mouse_event(_type, int(x), int(y), int(data), GetMessageExtraInfo())

#1 is one wheel scroll
def mouse_scroll(amount):
	mouse_event(WHEEL, 0, 0, int(amount * 120))

def key_down(virtualCode):
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 0, 0)

def key_up(virtualCode):
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 2, 0)

def key_hit(virtualCode, duration=0.02):
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 0, 0)
	sleep(duration / 2)
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 2, 0)
	sleep(duration / 2)

def enter():
	key_hit(VK_RETURN, duration=0.02)

def type_string(string, end="\n", interval=0.02):
	string += end
	for char in string:
		a = bytes(char, 'ascii')
		a = c_char(a)
		combined = CharToVk(a)
		low = combined & 0xff
		
		high = (combined>>8) & 0xff
		shift = high & 0x01
		cntrl = high & 0x02
		alt = high & 0x04

		if cntrl: key_down(VK_CONTROL)
		if alt: key_down(VK_MENU)
		if shift: key_down(VK_SHIFT)
		key_hit(low, duration=interval)
		if shift: key_up(VK_SHIFT)
		if alt: key_up(VK_MENU)
		if cntrl: key_up(VK_CONTROL)
		
