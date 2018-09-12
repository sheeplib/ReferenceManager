# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 17:44:14 2018

@author: sheeplib
"""

import urllib.request
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from tkinterhtml import HtmlFrame

root = tk.Tk()

li     = ['C','python','php','html','SQL','java']
movie  = ['CSS','jQuery','Bootstrap']
listb  = tk.Listbox(root)          #  创建两个列表组件
listb2 = tk.Listbox(root)
for item in li:                 # 第一个小部件插入数据
    listb.insert(0,item)
 
for item in movie:              # 第二个小部件插入数据
    listb2.insert(0,item)
 
listb.grid(row=0, column=0)                    # 将小部件放置到主窗口中
listb2.grid(row=1, column=0)

#frame = HtmlFrame(root, horizontal_scrollbar="auto")
frame = HtmlFrame(root)
#frame.grid(sticky=tk.NSEW)
frame.grid(row=0, column=1, rowspan=2) 

frame.set_content(urllib.request.urlopen("http://thonny.cs.ut.ee").read().decode())
#print(frame.html.cget("zoom"))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()