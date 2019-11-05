import ctypes as c
from ctypes.wintypes import *
from os import getppid

user32 = c.windll.user32
kernel32 = c.windll.kernel32
oleacc = c.windll.oleacc

DLL_FAIL_LOAD = 0x1
DLL_FAIL_FUNCTION = 0x2

class winlib_DLLFail():

    def __init__(self, dllname, funcname, code):
        self.code = code
        self.dllname = dllname
        self.funcname = funcname
    def getErrorCode(self):
        return self.code
    def getErrorMessage(self):
        if self.code == DLL_FAIL_LOAD:
            print("DLL<" + self.dllname + "> Failed to load. It either could not be found or is corrupt.")
        else:
            print("Function<" + self.funcname + "> is not a valid function in the dll <" + self.dllname + ">.")
            
class winlib_Window():
    def __init__(self, handle):
        self.handle = handle

    @property
    def title(self):
        length = user32.GetWindowTextLengthW(self.handle)
        buff = c.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(self.handle, buff, length + 1)
        return buff.value

    def getRect(self):
        result = (c.c_long * 4)()
        user32.GetWindowRect(self.handle, c.pointer(result))
        return tuple(result)

    def getPos(self):
        return self.getRect()[:2]

    def getChildren(self):
        arr = []
        def _enumProc(hwnd, lparam):
            win = winlib_Window(hwnd)
            arr.append(win)
        functype = c.WINFUNCTYPE(c.c_bool, c.POINTER(c.c_int), c.POINTER(c.c_int))
        user32.EnumChildWindows(self.handle, functype(_enumProc), 0)
        return arr

    def getHandleValue(self):
        p = c.cast(c.byref(self.handle), c.POINTER(c.c_long))
        return p.contents.value

    def __iter__(self):
        self._currentChildren = self.getChildren()
        self._childrenSize = len(self._currentChildren)
        self._childIndex = 0
        return self

    def __next__(self):
        if self._childIndex >= self._childrenSize:
            raise StopIteration
        else:
            r = self._currentChildren[self._childIndex]
            self._childIndex += 1
            return r

    def callFunc(self, name, *params, dll="user32", strfunc=False):
        handle = c.cdll.LoadLibrary(dll)
        print(params)
        if strfunc:
            name += "W"
        func = handle.__getattr__(name)
        func(self.handle, *params)

    def close(self):
        fail = user32.PostMessageW(self.handle, 0x0010, 0, 0)
        return fail != 0

    def getThreadId(self):
        return user32.GetWindowThreadProcessId(self.handle, None)
    
    def getProcessId(self):
        processId = DWORD()
        user32.GetWindowThreadProcessId(self.handle, c.pointer(processId))
        return processId.value

    def bringToTop(self):
        user32.SetWindowPos(self.handle, -1, 0, 0, 100, 100, 0x0001)

    def focus(self):
        user32.SetFocus(self.handle)

    def maximise(self):
        user32.PostMessageA(self.handle, 0x0112, 0xF030, 0)

    def minimise(self):
        user32.PostMessageA(self.handle, 0x0112, 0xF020, 0)

    def __str__(self):
        return "winlib.winlib_Window object: HWND(" + str(self.getHandleValue()) + "), TITLE(\"" + self.title + "\")"
""""
The function passed to hook must be:
def <name>(self, ncode, wparam, lparam):
"""
class HookFunction:
    def __init__(self, func, idHook):
        self.idHook = idHook
        self.func = func

    def hook(self, dwThreadId):
        self.c_func = GetHookFuncPointer(self.__hookProc)
        self.__hook = SetThreadHook_Raw(self.idHook, self.c_func, dwThreadId)

    def unhook(self):
        if self.__hook == -1: return
        user32.UnhookWindowsHookEx(self.__hook)
        self.__hook = -1
    
    def __hookProc(self, ncode, wparam, lparam):
        self.func(self, ncode, wparam, lparam)
        return user32.CallNextHookEx(self.__hook, ncode, wparam, lparam)
    
def SetThreadHook_Raw(idHook : int, func, dwThreadId):
    return user32.SetWindowsHookExA(idHook, func, kernel32.GetModuleHandleW(None), dwThreadId)

def GetHookFuncPointer(func):
    type = c.CFUNCTYPE(c.c_int, c.c_int, c.c_int, c.POINTER(c.c_void_p))
    return type(func)

def GetFunc_DLL(funcname, dll="user32"):
    
    d = None
    try:
        d = c.cdll.LoadLibrary(dll)
    except OSError:
        return winlib_DLLFail(dll, funcname, DLL_FAIL_LOAD)

    try:
        return d.__getattr__(funcname)
    except AttributeError:
        try:
            return d.__getattr__(funcname + "W")
        except AttributeError:
            return winlib_DLLFail(dll, funcname, DLL_FAIL_FUNCTION)

def CallFunc_DLL(funcname, *params, dll="user32"):

    d = None
    try:
        d = c.cdll.LoadLibrary(dll)
    except OSError:
        return winlib_DLLFail(dll, funcname, DLL_FAIL_LOAD)

    try:
        return d.__getattr__(funcname)(*params)
    except AttributeError:
        try:
            return d.__getattr__(funcname + "W")(*params)
        except AttributeError:
            return winlib_DLLFail(dll, funcname, DLL_FAIL_FUNCTION)

def SearchWindows(name : str):
    potentials = []
    def _enumProc(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = c.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)

            if name.lower().replace(" ", "") in buff.value.lower().replace(" ", ""):
                potentials.append(winlib_Window(hwnd))
        return True

    ftype = c.WINFUNCTYPE(c.c_bool, c.POINTER(c.c_int), c.POINTER(c.c_int))
    user32.EnumWindows(ftype(_enumProc), 0)
    
    return tuple(potentials)

def GetCurrentThreadId():
    return kernel32.GetCurrentThreadId()

def GetCurrentProcessId():
    return kernel32.GetCurrentProcessId()

def GetCurrentParentProcessId():
    return getppid()