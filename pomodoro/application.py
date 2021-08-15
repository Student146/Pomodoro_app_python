import tkinter as tk
from . import views as v
from . import widgets as w
import datetime
import time
from .images import ICONFILE

class Application(tk.Tk):
    def __init__(self, callbacks, focus_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callbacks = {'raise_start_window': self.raise_start_window,
                          'raise_running_window': self.raise_running_window,
                          'raise_notify_window': self.raise_notify_window,
                          'play_music': self.play_music,
                          'stop_music': self.stop_music,
                          'time_loop': self.time_loop,
                          'hide_window': self.hide_window,
                          'show_window': self.show_window}
        # get callbacks from the main pomotest.py
        # self.callbacks.update(callbacks)
        self.focus_manager = focus_manager
        self.widgets = dict()
        self.widgets['start_window'] = v.StartWindow(self,
                                                    self.callbacks,
                                                    focus_manager=self.focus_manager)
        self.widgets['start_window'].grid(row=0, padx=2, sticky='NSEW')
        self.start_window = self.widgets['start_window']
        self.widgets['running_window'] = v.RunningWindow(self, self.callbacks)
        self.widgets['running_window'].grid(row=0, padx=2, sticky='NSEW')
        self.running_window = self.widgets['running_window']
        self.widgets['notify_window'] = v.NotifyWindow(self,
                                                       self.callbacks,
                                                       focus_manager=self.focus_manager)
        self.widgets['notify_window'].grid(row=0, padx=2, sticky='NSEW')
        self.notify_window = self.widgets['notify_window']
        self.callbacks['raise_start_window']()
        # Sound manager
        self.sound_manager = w.SoundManager()

        # Icon for window
        self.taskbar_icon = tk.PhotoImage(file=ICONFILE)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        # Window title
        self.title('Pomodoro')

    def raise_start_window(self):
        """Start window will raise over running_window and notify_window"""
        self.widgets['start_window'].tkraise()
        self.cmd_text_get_focus() # so can type immediately

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

           Check the time and notify"""
        now = datetime.datetime.now()
        self.raise_running_window()
        data = self.get_data()
        notify_in_min = float(data['time'])
        added_time = datetime.timedelta(minutes=notify_in_min)
        notify_time = now + added_time
        while now < notify_time:
            time.sleep(1)
            now = datetime.datetime.now()
        self.focus_manager.record_previous_focus()
        self.raise_notify_window()
        self.play_music()
        self.show_window()
        self.snooze_button_get_focus()

    def cmd_text_get_focus(self):
        self.start_window.set_focus_cmd_text()

    def hide_window(self):
        """Minimize the window to taskbar icon"""
        # self.wm_state('iconic')
        self.iconify()

    def show_window(self):
        # self.attributes('-topmost', True)
        # self.focus_force()
        # self.wm_state('iconic')
        
        # self.wm_state('normal')
        self.deiconify()
        self.after(1, lambda: self.focus_force())
        # self.focus_force()
        # self.focus_force()

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