# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 21:29:05 2018

@author: sheeplib
"""
from tkinter.ttk import Notebook
from tkinter import *
import sys
import pydoc
 
def output_help_to_file(filepath, request):
    f = open(filepath, 'wt')
    sys.stdout = f
    pydoc.help(request)
    f.close()
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    #output_help_to_file('Notebook.txt', Notebook)
    output_help_to_file('Listbox.txt', Listbox)