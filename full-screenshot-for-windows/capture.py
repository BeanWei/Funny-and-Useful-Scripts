import win32api, win32con
import time
from PIL import ImageGrab

win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
time.sleep(0.5)
im=ImageGrab.grabclipboard()
im.save('1.png')