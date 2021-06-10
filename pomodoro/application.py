import tkinter as tk
from . import views as v
from . import widgets as w
import datetime
import time

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
                          'show_window': self.show_window}
        self.widgets = dict()
        self.widgets['start_window'] = v.StartWindow(self, self.callbacks)
        self.widgets['start_window'].grid(row=0, padx=2, sticky='NSEW')
        self.start_window = self.widgets['start_window']
        self.widgets['running_window'] = v.RunningWindow(self, self.callbacks)
        self.widgets['running_window'].grid(row=0, padx=2, sticky='NSEW')
        self.running_window = self.widgets['running_window']
        self.widgets['notify_window'] = v.NotifyWindow(self, self.callbacks)
        self.widgets['notify_window'].grid(row=0, padx=2, sticky='NSEW')
        self.notify_window = self.widgets['notify_window']
        self.callbacks['raise_start_window']()
        # Sound manager
        self.sound_manager = w.SoundManager()

    def raise_start_window(self):
        self.widgets['start_window'].tkraise()
        self.cmd_text_get_focus() # so can type immediately

    def raise_running_window(self):
        print('raise_running_window run')
        self.widgets['running_window'].tkraise()
        print('guess here')

    def raise_notify_window(self):
        self.widgets['notify_window'].tkraise()

    def play_music(self):
        self.sound_manager.play()

    def stop_music(self):
        self.sound_manager.stop()

    def get_data(self):
        return self.start_window.get_data()

    def time_loop(self):
        '''Logic part of the object

           Check the time and notify'''
        now = datetime.datetime.now()
        self.raise_running_window()
        data = self.get_data()
        notify_in_min = float(data['time'])
        added_time = datetime.timedelta(minutes=notify_in_min)
        notify_time = now + added_time
        while now < notify_time:
            time.sleep(1)
            now = datetime.datetime.now()
        self.raise_notify_window()
        self.play_music()
        self.show_window()
        self.snooze_button_get_focus()

    def cmd_text_get_focus(self):
        self.start_window.set_focus_cmd_text()

    def hide_window(self):
        # self.wm_state('iconic')
        self.withdraw()

    def show_window(self):
        # self.attributes('-topmost', True)
        # self.focus_force()
        # self.wm_state('iconic')
        self.wm_state('normal')
        self.deiconify()
        self.after(1, lambda: self.focus_force())
        # self.focus_force()
        # self.focus_force()

    def snooze_button_get_focus(self):
        self.notify_window.set_focus_snooze_button()