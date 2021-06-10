from pomodoro.application import Application
from pynput.keyboard import Key, Listener, KeyCode, Controller
from threading import Thread
import time

ALT_L_PRESSED = False

def on_press(key):
    global ALT_L_PRESSED
    print('{0} pressed'.format(
        key))
    # Controller.alt_pressed
    if key == Key.alt_l:
        ALT_L_PRESSED = True
    if key == KeyCode.from_char('p') and ALT_L_PRESSED:
        if app.state() == 'normal':
            app.hide_window()   
        else:
            # app.wm_state('iconic')
            # app.wm_state('normal')
            # root.attributes('-topmost', True)
            # app.focus_force()       
            # app.cmd_text_get_focus()
            # root.focus_force() #must type 2 times -> focus force
            app.show_window()
            app.cmd_text_get_focus()
        
def on_release(key):  
    global ALT_L_PRESSED
    print('{0} release'.format(
        key))
    if key == Key.alt_l:
        ALT_L_PRESSED = False
    if key == Key.esc:
        # Stop listener
        return False

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
