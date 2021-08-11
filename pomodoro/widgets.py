from pomodoro import audios
import tkinter as tk
from tkinter import scrolledtext
from pygame import mixer
from threading import Thread
from .audios import SOUNDFILE

class SoundManager:
    """Create object to play, pause, adjust sound volume"""
    def __init__(self):
        mixer.init()
        self.sound_manager = mixer.Sound(
            file=SOUNDFILE)
        # file='C://Users//ASUS//PycharmProjects//Pomodoro_app//pomodoro//audios//notification_iphong_ring.wav')
        self.sound_manager.set_volume(0.25)  # set volume the first time

    def play(self):
        self.sound_manager.play()

    def stop(self):
        self.sound_manager.stop()

    def set_volume(self, volume):
        self.sound_manager.set_volume(volume)

class CommandText(scrolledtext.ScrolledText):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.data = {'time': 0, 'message': ''}
        self.tag_configure('prompt', foreground='black')
        self.insert('end', '>>> ', ('prompt',))
        self.bind('<Return>', self.on_return)
        self.bind('<BackSpace>', self.on_delete)

    def on_return(self, *args):
        """Binding event when press 'Enter'"""
        cmd = self.get('prompt.last', 'end').strip()
        if cmd == '':
            self.data['time'] = 25
            self.data['message'] = 'No message'
        elif not cmd[0].isdigit(): # this is to write comment when needed, e.g >>> watch anime for 20 mins 
            self.insert('end', '\n>>> ', ('prompt',))
            return 'break'
        else:
            data = cmd.split(' ', maxsplit=1)
            self.data['time'] = data[0]
            try:
                self.data['message'] = data[1]
            except IndexError:
                self.data['message'] = 'No message'
        self.insert('end', '\n>>> ', ('prompt',))
        p1 = Thread(target=self.callbacks['time_loop'])
        p1.start()
        # self.callbacks['time_loop']() # the problem lie in here, in the loop, should in separate thread
        self.callbacks['hide_window']()
        return 'break'

    def on_delete(self, *args):
        """Binding event when press 'Backspace', not allow delete old data"""
        current_cursor_postion = self.index('prompt.last')
        current_cursor_postion_LINE = float(current_cursor_postion.split('.')[0])
        current_cursor_postion_CHAR = float(current_cursor_postion.split('.')[1])
        cursor_postion = self.index(tk.INSERT)
        cursor_postion_LINE = float(cursor_postion.split('.')[0])
        cursor_postion_CHAR = float(cursor_postion.split('.')[1])
        if cursor_postion_LINE < current_cursor_postion_LINE:
            print('True')
            return 'break'
        if cursor_postion_CHAR <= current_cursor_postion_CHAR:
            return 'break'

    def get_data(self):
        '''Return data in dictionary form {'time': 25, 'message': 'abc'}'''
        return self.data

class ValidateMixin:
    """Provide validate function to widget"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
