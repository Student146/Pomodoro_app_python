from pomodoro.application import Application
from pynput.keyboard import Key, Listener, KeyCode, Controller
from threading import Thread
import ctypes

ALT_L_PRESSED = False
set_to_foreground = ctypes.windll.user32.SetForegroundWindow
keybd_event = ctypes.windll.user32.keybd_event

alt_key = 0x12
extended_key = 0x0001
key_up = 0x0002

def on_press(key):
    global ALT_L_PRESSED
    print('{0} pressed'.format(
        key))
    print(app.state())
    print("focus is:", app.focus_get())
    # Controller.alt_pressed
    if key == Key.alt_l:
        ALT_L_PRESSED = True
    if key == Key.f9:                      
        if app.state() == 'normal' and app.focus_get() is None:
            print('the window is losing focus')
            app.iconify()
        if app.state() == 'iconic':
            app.attributes('-topmost', True)
            app.deiconify()
            app.attributes('-topmost', False)
            keybd_event(alt_key, 0, extended_key | 0, 0)
            set_to_foreground(app.winfo_id())
            keybd_event(alt_key, 0, extended_key | key_up, 0)
            print("focus is:", app.focus_get())
            
            print("focus is:", app.focus_get())
            app.focus_cmd_text()
            print("focus is:", app.focus_get())
        else:
            app.iconify()   
        
def on_release(key):  
    global ALT_L_PRESSED
    print('{0} release'.format(
        key))
    if key == Key.alt_l:
        ALT_L_PRESSED = False
    # if key == Key.esc:
    #     # Stop listener
    #     return False

def run_listener():
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
    # code to run listener, work as while True:           
    # put into function to use thread

app = Application()
app.cmd_text_get_focus()
p1 = Thread(target=run_listener, daemon=True)  # daemon=True -> when terminate, terminate too
p1.start()
app.mainloop()           
