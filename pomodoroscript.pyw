import datetime
import time
import tkinter as tk
from tkinter import ttk
import winsound
import subprocess



class PopupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('500x200')
        self.title('Pomodoro')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.button = tk.Button(self, text='Snooze', command=self.on_click, height=20, width=40,
                                background='blue')
        self.button.grid(column=0, row=0)
        self.button.focus_set()
        # when focus set -> user only need press enter -> can snooze

    def on_closing(self):
        user_respond = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\user_respond_data.txt', 'w')
        user_respond.write('state close')
        user_respond.close()
        winsound.PlaySound(None,
                           winsound.SND_ASYNC | winsound.SND_LOOP)
        self.destroy()

    def on_click(self):
        user_respond = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\user_respond_data.txt', 'w')
        user_respond.write('state snooze')
        user_respond.close()
        winsound.PlaySound(None,
                           winsound.SND_ASYNC | winsound.SND_LOOP)
        PopupWindow.restore_volume()
        self.destroy()

    @staticmethod
    def change_volume():
        """Change the current volume to 30% so not loudy"""
        p = subprocess.run(['C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe', '-ExecutionPolicy',
                            'Unrestricted', '-WindowStyle', 'Hidden',
                            '& "C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\changevolume.ps1"'])

    @staticmethod
    def restore_volume():
        """Change current volume to 100%"""
        p = subprocess.run(['C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe', '-ExecutionPolicy',
                            'Unrestricted', '-WindowStyle', 'Hidden',
                            '& "C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\changevolume100.ps1"'])


class StartWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.taskbar_icon = tk.PhotoImage(file='C:\\Users\\ASUS\\PycharmProjects\\pomodoro\\pomodoro\\images\\pomodoro_image.png')
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        # above 2 lines code to make Window icon
        self.geometry('500x200')
        self.title('Pomodoro')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        # when close windows -> terminate the program
        self.widgets = dict()
        self.widgets['Label1'] = ttk.Label(master=self, text='Choose when to notify: ')
        self.widgets['Label1'].grid(column=0, row=0)

        self.widgets['Given time'] = ttk.Combobox(master=self, text='Choose when to notify',
                                                  values=(1, 5, 10, 15, 20, 25),
                                                  state='readonly',
                                                  font=('Arial', 15)
                                                  )
        self.widgets['Given time'].grid(column=0, row=1)

        self.widgets['Message_entry'] = ttk.Entry(master=self)
        self.widgets['Message_entry'].grid(column=0, row=3)

        self.widgets['Choose'] = ttk.Button(master=self, text='Select', command=self.on_click)
        self.widgets['Choose'].grid(column=0, row=4)

    def on_click(self):
        """return data: create data package in .txt and close the windows"""
        time_data = self.widgets['Given time'].get()
        message_data = self.widgets['Message_entry'].get()
        if message_data == '':
            message_data = 'None'
        data_file = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\time_data.txt', 'w')
        data_file.write('time ' + time_data + '\n')
        data_file.write('message ' + message_data + '\n')
        data_file.write('state open')
        data_file.close()
        self.destroy()

    def on_closing(self):
        user_respond = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\time_data.txt', 'w')
        user_respond.write('state close')
        user_respond.close()
        self.destroy()


def notify():
    """combine add_time() with sleep() method to check"""
    a = datetime.datetime.now()
    data = get_data_in('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\time_data.txt')
    notify_in_sec = 30
    notify_in_min = int(data['time'])
    added_time = datetime.timedelta(minutes=notify_in_min)
    b = a + added_time
    print(b)
    while a < b:
        time.sleep(1)
        a = datetime.datetime.now()
    PopupWindow.change_volume()  # This method change volume to 30%
    winsound.PlaySound("C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\554316__franco1904__clock-iphone.wav",
                       winsound.SND_ASYNC | winsound.SND_LOOP)
    popup = PopupWindow()
    popup.attributes('-topmost', True)
    # raise the notification window on top of other windows
    popup.focus_force()
    # take the focus to notification window so can press 'Space' bar to snooze the app
    popup.mainloop()


def get_data_in(filepath):
    """Take data from text file and return the dictionary in form {'data category' : 'data'}"""
    fin = open(filepath, 'r')
    data = dict()
    for line in fin:
        data_in_line = line.strip().split()
        data_field = data_in_line[0]
        value = data_in_line[1]
        data[data_field] = value
    return data


# def test_data_transfer():
#     data = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\test_data_transfer.txt', 'w')
#     data.write('snooze')
#     data.close()
#     fin = open('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\test_data_transfer.txt', 'r')
#     a = fin.readline()
#     print(repr(a))
#     # ok, result is print -> 'snooze' not 'snooze\n'


def main():
    state_on = True
    while state_on:
        a = StartWindow()
        a.mainloop()
        message = get_data_in('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\time_data.txt')
        if message['state'] == 'close':
            break
        notify()
        message = get_data_in('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\user_respond_data.txt')
        if message['state'] == 'close':
            break


# def test_main():
#     a = StartWindow()
#     a.mainloop()
#     b = get_data_in('C:\\Users\\ASUS\\OneDrive - hus.edu.vn\\Desktop\\time_data.txt')
#     print(b)


if __name__ == '__main__':
    main()
