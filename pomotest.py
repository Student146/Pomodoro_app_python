from pomodoro.application import Application
from pynput.keyboard import Key, Listener, KeyCode, Controller
from threading import Thread
import ctypes
from win32gui import GetWindowText, GetForegroundWindow
import win32gui
from pomodoro.widgets import FocusManager

ALT_L_PRESSED = False
previous_focus_app = ''
set_to_foreground = ctypes.windll.user32.SetForegroundWindow
keybd_event = ctypes.windll.user32.keybd_event

alt_key = 0x12
extended_key = 0x0001
key_up = 0x0002

focus_manager = FocusManager()

def give_back_focus_old_app():
    global previous_focus_app
    print('Pervious focus app: ', previous_focus_app)
    handle = win32gui.FindWindow(0, previous_focus_app)   
    win32gui.SetForegroundWindow(handle)
    print('give back focus function run')

def on_press(key):
    global ALT_L_PRESSED, previous_focus_app, focus_manager
    print('{0} pressed'.format(key))
    print(app.state())
    # app.state() can be normal, icon,...
    print("focus is in pomo?:", app.focus_get())
    # focus is: None | .!startwindow.!frame
    # WindowText is Pomodoro
    # Controller.alt_pressed
    if key == Key.alt_l:
        ALT_L_PRESSED = True
    if key == Key.f9:        
        if app.state() == 'normal' and app.focus_get() is None:
            focus_manager.return_focus()
            print('the window is losing focus')
            app.iconify()
        if app.state() == 'iconic':
            focus_manager.record_previous_focus()
            app.attributes('-topmost', True)
            app.deiconify()
            app.attributes('-topmost', False)
            keybd_event(alt_key, 0, extended_key | 0, 0)
            set_to_foreground(app.winfo_id())
            # handle = win32gui.FindWindow(0, "Pomodoro")   
            # win32gui.SetForegroundWindow(handle) 
            keybd_event(alt_key, 0, extended_key | key_up, 0)
             

            print("focus is:", app.focus_get())
            
            app.focus_cmd_text()
            print("focus is:", app.focus_get())
            print()
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

#callbacks = {'give_back_focus_old_app': give_back_focus_old_app}
callbacks = dict()
app = Application(callbacks, focus_manager=focus_manager)
app.cmd_text_get_focus()
p1 = Thread(target=run_listener, daemon=True)  # daemon=True -> when terminate, terminate too
p1.start()
app.mainloop()           
