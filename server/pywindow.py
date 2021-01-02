import win32gui as gui
import win32api as api
import win32con as con
import win32com as com
import win32ui as ui
from win32 import win32process
import psutil as util
import time


hwnd_title = []
hidden_title = []


def is_window(hwnd):
    if (gui.IsWindow(hwnd) and
        gui.IsWindowEnabled(hwnd) and
            gui.IsWindowVisible(hwnd)):
        return True
    else:
        return False


def is_window_legal(hwnd):
    if gui.IsWindow(hwnd) and gui.IsWindowEnabled(hwnd):
        return True
    else:
        return False


def get_windowstate(hwnd):
    statu = "正常"
    if not gui.IsWindowVisible(hwnd):
        statu = "隐藏"
    if gui.IsIconic(hwnd):
        statu = "最小化"
    if (gui.GetWindowLong(hwnd, con.GWL_EXSTYLE) & con.WS_EX_TOPMOST) != 0:
        statu = "置顶"
    if gui.GetForegroundWindow() == hwnd:
        statu = "活动窗口"
    return statu


def find_window(hwnd):
    for it, val in enumerate(hwnd_title):
        if(hwnd == val['hwnd']):
            return it
    return None


def get_winprocess(hwnd):
    thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    process = util.Process(process_id)
    return process_id, process.name()


def get_windowtext(hwnd):
    windowtext = gui.GetWindowText(hwnd)
    if len(windowtext) == 0 or windowtext == " ":
        return None
    return windowtext


def getWindowSize(hwnd):
    left, top, right, bottom = gui.GetWindowRect(hwnd)
    return {
        'left': left,
        'top': top,
        'width': right-left,
        'height': bottom-top
    }


def get_hwndinfor(hwnd):
    pid, proc = get_winprocess(hwnd)
    return{
        "hwnd": hwnd,
        "title": get_windowtext(hwnd),
        "pid": pid,
        "proc": proc,
        "size": getWindowSize(hwnd),
        "state": get_windowstate(hwnd)
    }


def get_all_hwnd(hwnd, param):
    if is_window(hwnd):
        inf = get_hwndinfor(hwnd)
        if inf['title'] is not None:
            hwnd_title.append(inf)


def get_all_window(hwnd=0):
    hwnd_title.clear()
    gui.EnumWindows(get_all_hwnd, 0)
    for i in hidden_title:
        if is_window_legal(i):
            f = find_window(i)
            if f is None:
                inf = get_hwndinfor(i)
                hwnd_title.append(i)
    return hwnd_title


def getText(hwnd):
    if hwnd == 0:
        return 'hwnd is not used return 0'
    length = 10000
    buf = gui.PyMakeBuffer(length)
    length2 = gui.SendMessage(hwnd, con.WM_GETTEXT, length, buf)+1
    buf = gui.PyMakeBuffer(length2)
    gui.SendMessage(hwnd, con.WM_GETTEXT, length2, buf)
    address, length = gui.PyGetBufferAddressAndLen(buf)
    text = gui.PyGetString(address, length)
    return text


def updatewindow(hwnd=0):
    i = find_window(hwnd)
    if i is not None:
        inf = get_hwndinfor(hwnd)
        hwnd_title[i] = inf
    else:
        get_all_window()


def getforewindow(hwnd=0):
    cur = gui.GetForegroundWindow()
    return cur


def setforewindow(hwnd):
    if is_window(hwnd):
        gui.ShowWindow(hwnd, con.SW_SHOWNORMAL)
        gui.SetForegroundWindow(hwnd)
        updatewindow(hwnd)


def tabforwindow(hwnd=0):
    cur = getforewindow()
    i = find_window(cur)
    print(i)
    try:
        if i is not None:
            setforewindow(hwnd_title[(i+1) % len(hwnd_title)]['hwnd'])
            updatewindow(cur)
        else:
            if len(hwnd_title) > 0:
                setforewindow(hwnd_title[0]['hwnd'])
                updatewindow(cur)
            else:
                get_all_window()
    except:
        pass


def minwindow(hwnd):
    if is_window(hwnd):
        gui.ShowWindow(hwnd, con.SW_MINIMIZE)
        updatewindow(hwnd)


def maxwindow(hwnd):
    if is_window(hwnd):
        gui.ShowWindow(hwnd, con.SW_MAXIMIZE)
        updatewindow(hwnd)


def norwindow(hwnd):
    if is_window_legal(hwnd):
        gui.ShowWindow(hwnd, con.SW_SHOWNORMAL)
        for iter, val in enumerate(hidden_title):
            if val == hwnd:
                del hidden_title[iter]
        updatewindow(hwnd)


def restorewindow(hwnd):
    if is_window_legal(hwnd):
        if gui.IsWindowVisible(hwnd):
            gui.ShowWindow(hwnd, con.SW_SHOWNORMAL)
        else:
            gui.ShowWindow(hwnd, con.SW_RESTORE)
        for iter, val in enumerate(hidden_title):
            if val == hwnd:
                del hidden_title[iter]
        updatewindow(hwnd)


def ztopwindow(hwnd):
    if is_window(hwnd):
        rect = getWindowSize(hwnd)
        gui.SetWindowPos(hwnd, con.HWND_TOPMOST,
                         rect['left'], rect['top'], rect['width'], rect['height'], con.SWP_SHOWWINDOW)
        updatewindow(hwnd)


def zcancelwindow(hwnd):
    if is_window(hwnd):
        rect = getWindowSize(hwnd)
        gui.SetWindowPos(hwnd, con.HWND_NOTOPMOST,
                         rect['left'], rect['top'], rect['width'], rect['height'], con.SWP_SHOWWINDOW)
        updatewindow(hwnd)


def inviswindow(hwnd):
    if is_window(hwnd):
        gui.ShowWindow(hwnd, con.SW_HIDE)
        hidden_title.append(hwnd)
        updatewindow(hwnd)


def offwindow(hwnd):
    if is_window_legal(hwnd):
        gui.PostMessage(hwnd, con.WM_CLOSE, 0, 0)
        updatewindow(hwnd)


def offpid(hwnd):
    if is_window_legal(hwnd):
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        try:
            process = util.Process(process_id)
            process.kill()
        except:
            pass
        else:
            i = find_window(hwnd)
            if i is not None:
                del hwnd_title[i]
        updatewindow(hwnd)


def default(hwnd=0):
    print("no kind of this window operate")


switch = {
    "all": get_all_window,
    "get": getforewindow,
    "set": setforewindow,
    "min": minwindow,
    "max": maxwindow,
    "nor": norwindow,
    "tab": tabforwindow,
    "top": ztopwindow,
    "ctop": zcancelwindow,
    "res": restorewindow,
    "inv": inviswindow,
    "offw": offwindow,
    "offp": offpid
}


def windowreset():
    for i in hidden_title:
        if is_window_legal(i):
            norwindow(i)
            
def operate(data):
    switch.get(data.get('operate'), )(data.get('hwnd'))
    return {'kind': 's', 'data': hwnd_title}


if __name__ == '__main__':
    x = {'operate': 'get', 'hwnd': 131860}
    a = operate(x)
    print(a)

    # get_all_window()
    # for i in hwnd_title:
    #     print(i)
    # while True:
    #     point = api.GetCursorPos()
    #     print(point)
    #     x = gui.WindowFromPoint(point)
    #     curtext=getText(x)
    #     print(x,curtext)
    #     parent=gui.GetParent(x)
    #     parenttext = getText(parent)
    #     print(parent,parenttext)
    #     # topparent=gui.GetTopWindow(x)
    #     # toptext=getText(topparent)
    #     # print(topparent,toptext)
    #     time.sleep(2)
