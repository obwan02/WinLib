import winlib
import keyboard_funcs as k

def HookFunc(self, ncode, wparam, lparam):
    if wparam != 0x0100:
        return

    if lparam[0] == k.VK_F2:
        self.UninstallHook()
        HOOK = 0

    shift = k.GetKeyState(k.VK_SHIFT)[0]
    caps_lock = k.GetKeyState(k.VK_CAPITAL)[1]
    caps = shift ^ caps_lock
    
    char = k.ToAscii(lparam[0], lparam[1], lparam[2])
    if caps:
        char = char.upper()
    print(bin(caps_lock) + ", " + bin(shift))
    return


HOOK = winlib.HookFunction(HookFunc, 13)
HOOK.HookIntoThread(0)
if HOOK:
    print("Installed. ")
    msg = winlib.c.wintypes.MSG()
    winlib.user32.GetMessageA(winlib.c.byref(msg), 0, 0, 0)
