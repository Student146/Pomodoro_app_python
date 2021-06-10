import tkinter as tk
from tkinter import ttk
import inspect

root = tk.Tk()
a = ttk.Label(root)
b = str(type(a)) in ("<class 'tkinter.ttk.Label'>", )
print(a.__class__)
print(ttk.Label().__class__)
print(a.__class__ in (ttk.Label.__class__,))
print(b)
print(type(a))
print('======================')
print('try inspect')
print(isinstance(a, ttk.Label))
# use isinstance to check the widget is of ttk.Label or not