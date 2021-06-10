import tkinter as tk

def on_click():
    print(root.state())

root = tk.Tk()
button = tk.Button(root, text='click', command=on_click)
button.pack()
root.mainloop()