import tkinter as tk
from . import views as v
from . import widgets as w
import datetime
import time
from .images import ICONFILE, TRAYICON_FILE_PATH
from pynput.keyboard import Key, Listener
from win32gui import GetWindowText, GetForegroundWindow, FindWindow, SetForegroundWindow
from threading import Thread
from PySimpleGUIQt import SystemTray


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callbacks = {'raise_start_window': self.raise_start_window,
                          'raise_running_window': self.raise_running_window,
                          'raise_notify_window': self.raise_notify_window,
                          'play_music': self.play_music,
                          'stop_music': self.stop_music,
                          'time_loop': self.time_loop,
                          'hide_window': self.hide_window,
                          'show_window': self.show_window,
                          'return_focus_to_previous_window': self.return_focus_to_previous_window}
        # get callbacks from the main pomotest.py
        # self.callbacks.update(callbacks)
        self.widgets = dict()
        self.widgets['start_window'] = v.StartWindow(self,
                                                    self.callbacks
                                                    )
        self.widgets['start_window'].grid(row=0, padx=2, sticky='NSEW')
        self.start_window = self.widgets['start_window']
        self.widgets['running_window'] = v.RunningWindow(self, self.callbacks)
        self.widgets['running_window'].grid(row=0, padx=2, sticky='NSEW')
        self.running_window = self.widgets['running_window']
        self.widgets['notify_window'] = v.NotifyWindow(self,
                                                       self.callbacks
                                                       )
        self.widgets['notify_window'].grid(row=0, padx=2, sticky='NSEW')
        self.notify_window = self.widgets['notify_window']
        self.callbacks['raise_start_window']()

        # Keyboard listener
        self.keyboard_listener = Listener(on_press=self.on_press, 
                                          on_release=self.on_release)
        self.keyboard_listener.start()

        # Sound manager
        self.sound_manager = w.SoundManager()

        # Icon for window
        self.taskbar_icon = tk.PhotoImage(file=ICONFILE)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        # Window title
        self.title('Pomodoro')

        # Record for previous window has focus
        self.current_focused_app_name = 'Pomodoro'
        self.previous_focused_window_name = 'Pomodoro'

        # Current window record
        self.current_window_in_root = 'start_window'

        # Window manager
        # Window manager will manage: set focus to element,... when that window float up
        # eg: when start_window is current on top -> text will get focus
        # if notify_window on top -> snooze button will get focus
        self.window_manager = {
            'start_window': self.cmd_text_get_focus,
            'running_window': self.running_window_get_focus,
            'notify_window': self.snooze_button_get_focus
        }

        # Application tray icon to notify that pomodoro is running
        self.tray_icon_appeared = True
        self.SYSTEM_TRAY_ICON = ICONFILE

    def on_press(self, key):
        """This method record key pressed of keyboard listener"""
        print('alphanumeric key {0} pressed'.format(key))
        print('Focus in window: ', self.focus_get())
        print('Window state: ', self.state())
        print('Current has focus window name: ', GetWindowText(GetForegroundWindow()))
        if key == Key.f9:
            self.current_focused_app_name = GetWindowText(GetForegroundWindow())
            if self.state() == 'iconic':
                self.show_window()
            elif self.state() == 'normal' and self.current_focused_app_name != 'Pomodoro':
                # this case when the pomo is behind the other window
                self.iconify() # bad programming behaviour
                self.show_window()
            else:
                self.hide_window()

    def on_release(self, key):
        """This method record key release of keyboard listener"""
        print('{0} released'.format(key))
        print()

    def hide_window(self):
        """Minimize the window to taskbar icon"""
        self.iconify()
        if self.previous_focused_window_name != 'Pomodoro':
            self.return_focus_to_previous_window()

    def show_window(self):
        """Restore ROOT window from taskbar icon -> window + get focus on the root window -> '.'"""
        self.set_previous_focused_window_name()
        if self.current_focused_app_name != 'Pomodoro':
            self.deiconify()
            self.iconify()
            self.deiconify()
            self.window_manager[self.current_window_in_root]()
        else:
            self.deiconify()
            self.window_manager[self.current_window_in_root]()
    
    def return_focus_to_previous_window(self):
        """When pomodoro run, will steal focus, eg, when we reading in chrome
        we will record chrome and turn back focus to chrome after set alarm"""
        handle = FindWindow(0, self.previous_focused_window_name)   
        SetForegroundWindow(handle)

    def set_current_focused_app_name(self):
        """Current focused app name is used to check if pomo currently have focus
        or not"""
        self.current_focused_app_name = GetWindowText(GetForegroundWindow())

    def set_previous_focused_window_name(self):
        """Previous focused window name is the window have focus before
        pomodoro steal focus, eg Chrome, Zim,..."""
        self.previous_focused_window_name = GetWindowText(GetForegroundWindow())

    def raise_start_window(self):
        """Start window will raise over running_window and notify_window"""
        self.widgets['start_window'].tkraise()
        self.cmd_text_get_focus() # so can type immediately
        self.current_window_in_root = 'start_window'

    def raise_running_window(self):
        """Running_window will raise over start_window and notify_window"""
        print('raise_running_window run')
        self.widgets['running_window'].tkraise()

    def raise_notify_window(self):
        """Notify_window will raise on top of Frame"""
        self.widgets['notify_window'].tkraise()

    def play_music(self):
        self.sound_manager.play()

    def stop_music(self):
        self.sound_manager.stop()

    def get_data(self) -> dict:
        """Get user input data in the form dict: {'message': 'abc', ...}"""
        return self.start_window.get_data()

    def time_loop(self):
        """Logic part of the object

           Check the time and notify
           
           This method is run by a separate thread in the background"""
        now = datetime.datetime.now()

        self.raise_running_window()
        self.current_window_in_root = 'running_window'
        tray = SystemTray(filename=self.SYSTEM_TRAY_ICON, tooltip='Pomodoro is running...')

        data = self.get_data()
        notify_in_min = float(data['time'])
        time.sleep(notify_in_min*60)

        # When time is over
        self.raise_notify_window()
        self.current_window_in_root = 'notify_window'
        self.play_music()
        self.show_window()
        # self.snooze_button_get_focus()

    def cmd_text_get_focus(self):
        """Set focus to text widget to type immediately"""
        self.start_window.set_focus_cmd_text()

    def snooze_button_get_focus(self):
        """Will focus to the snooze_button in notify_window
        
        Get focus to quickly press by 'Spacebar'"""
        self.notify_window.set_focus_snooze_button()

    #this method is use to test, test if after deiconify, the application has
    #focus or not, now it return ".", now I want to get focus to start_window
    #if it return .!startwindow, it will very good
    def focus_start_window(self):
        self.start_window.focus_set()

    def focus_cmd_text(self):
        #self.start_window.set_focus_cmd_text()
        self.start_window.set_focus_cmd_text()

    def running_window_get_focus(self):
        pass

    # def tray_icon_run_thread(self):
    #     """Function to use Thread to display icon, because Icon.run() is not a thread, will stop the program"""
    #     tray = SystemTray(filename=self.SYSTEM_TRAY_ICON)
    #     while self.tray_icon_appeared:
    #         pass 

    # def tray_icon_run(self):
    #     """Make tray icon display in a thread"""
    #     tray_icon_thread = Thread(target=self.tray_icon_run_thread)
    #     tray_icon_thread.start()

    # def tray_icon_stop(self):
    #     """Stop displaying the tray icon in taskbar"""
    #     self.tray_icon_appeared = False