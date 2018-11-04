from ctypes import *
from time import sleep
from winlib.defs import *

user32 = windll.user32
VirtualToScan = lambda vk: user32.MapVirtualKeyA(vk, 0)
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

mapKeys = {
	"a" : KEY_A,
	"b" : KEY_B,
	"c" : KEY_C,
	"d" : KEY_D,
	"e" : KEY_E,
	"f" : KEY_F,
	"g" : KEY_G,
	"h" : KEY_H,
	"i" : KEY_I,
	"j" : KEY_J,
	"k" : KEY_K,
	"l" : KEY_L,
	"m" : KEY_M,
	"n" : KEY_N,
	"o" : KEY_O,
	"p" : KEY_P,
	"q" : KEY_Q,
	"r" : KEY_R,
	"s" : KEY_S,
	"t" : KEY_T,
	"u" : KEY_U,
	"v" : KEY_V,
	"w" : KEY_W,
	"x" : KEY_X,
	"y" : KEY_Y,
	"z" : KEY_Z,
	"\t" : VK_TAB,
	"\n" : VK_RETURN,
	" " : VK_SPACE,
	"0" : KEY_0,
	"1" : KEY_1,
	"2" : KEY_2,
	"3" : KEY_3,
	"4" : KEY_4,
	"5" : KEY_5,
	"6" : KEY_6,
	"7" : KEY_7,
	"8" : KEY_8,
	"9" : KEY_9,

	"-" : VK_SUBTRACT,
	"'" : VK_OEM_7
}

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

def simulate_keyhit(virtualCode, duration=0.02):
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 0, 0)
	sleep(duration / 2);
	user32.keybd_event(virtualCode, VirtualToScan(virtualCode), 2, 0)
	sleep(duration / 2)

def type_string(string, end="\n"):
	for char in string:
		c = mapKeys[char.lower()]
		if char.lower() != char:
			#is a capital letter
			simulate_keyhit(VK_CAPITAL)
			simulate_keyhit(mapKeys[char.lower()]);
			simulate_keyhit(VK_CAPITAL);
		else:
			simulate_keyhit(mapKeys[char.lower()]);
	simulate_keyhit(mapKeys[end.lower()])


