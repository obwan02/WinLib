import winlib
import keyboard_funcs as k

def HookFunc(ncode, wparam, lparam):
    global HOOK

    if wparam != 0x0100:
        return winlib.user32.CallNextHookEx(HOOK, ncode, wparam, lparam)

    if lparam[0] == 0x25:
        user32.UninstallWindowsHookEx(HOOK)
        HOOK = 0

    caps = False
    if k.GetKeyState(k.VK_SHIFT):
        caps = not caps
    if k.GetKeyState(k.VK_CONTROL):
        caps = not caps
        
    char = k.ToAscii(lparam[0], lparam[1], lparam[2])
    if caps:
        char = char.upper()
    print(char, end="")
    return winlib.user32.CallNextHookEx(HOOK, ncode, wparam, lparam)

func = winlib.GetHookFuncPointer(HookFunc)
HOOK = winlib.SetHook(13, func, 0)

if HOOK:
    print("Installed. ")
    msg = winlib.c.wintypes.MSG()
    winlib.user32.GetMessageA(winlib.c.byref(msg), 0, 0, 0)
