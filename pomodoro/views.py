import tkinter as tk
from . import widgets as w

class StartWindow(tk.Frame):
    """Start window has field to write time, button to choose time, field to write message"""
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.widgets = {}
        '''self.widgets = {'input_time': tk.Entry, ...}'''

        self.callbacks = callbacks
        # callbacks to application.py method

        # the data should have in application.py

        # self.widgets['input_time_label'] = tk.Label(self, text='When to notify: ')
        # self.widgets['input_time_label'].grid(column=0, row=0)

        # self.widgets['input_time_entry'] = tk.Entry(self, variable=tk.StringVar)
        # self.widgets['input_time_entry'].grid(column=0, row=1)

        # self.widgets['select_button'] = tk.Button(self, text='Select')
        # self.widgets['select_button'].grid(column=1, row=1)

        # self.widgets['1min_button'] = tk.Button(self, text='1 min')
        # self.widgets['1min_button'].grid(column=0, row=2)

        # self.widgets['5min_button'] = tk.Button(self, text='5 min')
        # self.widgets['5min_button'].grid(column=1, row=2)

        # self.widgets['message_label'] = tk.Label(self, text='Message: ')
        # self.widgets['message_label'].grid(column=0, row=3)

        # self.widgets['message_entry'] = tk.Entry(self, variable=tk.StringVar)
        # self.widgets['message_entry'].grid(column=1, row=3)
        self.widgets['cmd_text'] = w.CommandText(self, self.callbacks)
        self.widgets['cmd_text'].grid(column=0, row=0)
        

    def on_select(self):
        """run when clicked Select button"""
        message = self.widgets['message_entry'].get()
        self.data_model.set_message(message)
        user_input_time = int(self.widgets['input_time_entry'].get())
        self.data_model.set_user_input_time(user_input_time)
        # self.callbacks['tk raise to standby screen appear']

    def get_data(self):
        """return all data in this frame in form dict eg {'message': 'abc',...}"""
        data = self.widgets['cmd_text'].get_data()
        # for key, widget in self.widgets.items():
        #     if isinstance(self.widgets[key], tk.Entry):
        #         data[key] = widget.get()
        return data

    def set_focus_cmd_text(self):
        self.widgets['cmd_text'].focus_set()


class RunningWindow(tk.Frame):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg='blue')
        self.widgets = {}
        '''self.widgets = {'input_time': tk.Entry, ...}'''
        self.callbacks = callbacks
        self.widgets['Running_label'] = tk.Label(self, text='Pomodoro is running')
        self.widgets['Running_label'].grid(row=0)


class NotifyWindow(tk.Frame):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.widgets = {}
        '''self.widgets = {'input_time': tk.Entry, ...}'''

        self.callbacks = callbacks
        self.widgets['Snooze_button'] = tk.Button(self, text='Snooze', command=self.on_snooze)
        self.widgets['Snooze_button'].grid(row=0)

    def on_snooze(self):
        # will silent the SoundManager, raise the StartWindow
        self.callbacks['stop_music']()
        self.callbacks['raise_start_window']()

    def set_focus_snooze_button(self):
        self.widgets['Snooze_button'].focus_set()
        self.widgets['Snooze_button'].focus_force()