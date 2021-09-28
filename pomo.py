from pomodoro.application import Application
from ctypes import windll

# this line to make the window not blurr
windll.shcore.SetProcessDpiAwareness(1)

app = Application()
app.mainloop()           
