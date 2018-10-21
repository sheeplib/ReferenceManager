# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:44:11 2018

@author: sheeplib

App主程序
"""

from Interface import *
from Item import *
from tkinter import *
from tkinter import filedialog
import pickle

class Application(UI):
    def __init__(self, master = None):
        UI.__init__(self,master)
        self.__createEvents()
        self.tlib = Tlibrary()
        self.currenttitle = None
        self.filename = 'test.bib'
        self.cachefile = 'bibcache.sav'
        self.autoload()
        self.updatethesislistwithtlib()
        self.updatewithcurrentitem()
    def __createEvents(self):
        self.l_listlist.bind("<Double-Button-1>", self.selectthesis)
        self.r_buttonreflash.bind('<ButtonRelease-1>', self.updatewindow)
        self.r_buttonmodify.bind('<ButtonRelease-1>', self.updatetotlibdata)
        self.l_buttonloadbib.bind('<ButtonRelease-1>', self.openbibfile)
        self.l_buttonsavebib.bind('<ButtonRelease-1>', self.savebibfile)
        self.r_buttoncreate.bind('<ButtonRelease-1>', self.createrecord)
        pass
    def createrecord(self, msg=None):
        self.tlib.selectdefault()
        self.updatewithcurrentitem()
    def updatewindow(self, msg=None):
        self.updatethesislistwithtlib()
        self.updatewithcurrentitem()
    def updatethesislistwithtlib(self): # 用数据中的内容更新列表
        self.l_listlist.delete(0, END)
        for title in self.tlib.titlelist():
            self.l_listlist.insert(END, title)
    def selectthesis(self, msg=None): # 选择文章
        index = self.l_listlist.curselection()
        #print(str(type(index))+str(index))
        if len(index) <= 0:
            self.tlib.selectdefault()
            return 0
        title = self.l_listlist.get(index[0])
        self.tlib.select(title)
        #self.currenttitle = title
        #self.updatewithtlibdata()
        self.updatewithcurrentitem()
    def updatewithcurrentitem(self, msg=None):
        for table in self.basetable:
            table.box.delete(1.0,END)
            text = self.tlib.curitem.base[table.label]
            table.box.insert(END, text)
        for table in self.notetable:
            table.box.delete(1.0,END)
            text = self.tlib.curitem.note[table.label]
            table.box.insert(END, text)
        self.r_codebox.delete(1.0, END)
        self.r_codebox.insert(END, self.tlib.curitem.code)
        #print('debug:'+str(self.r_tab.tabs())+str(self.r_codeframe))############
    def updatewithtlibdata(self, msg=None):
        if self.currenttitle:
            label = self.tlib.getlabel(self.currenttitle)
        for table in self.basetable:
            table.box.delete(1.0,END)
            text = self.tlib[label].base[table.label]
            table.box.insert(END, text)
        for table in self.notetable:
            table.box.delete(1.0,END)
            text = self.tlib[label].note[table.label]
            table.box.insert(END, text)
        self.r_codebox.delete(1.0, END)
        self.r_codebox.insert(END, self.tlib[label].code)
    def updatetotlibdata(self, msg=None):
        #print(self.r_tab.select()+'=='+str(self.r_codeframe))
        if str(self.r_tab.select()) == str(self.r_codeframe):
            self.tlib.addbibrecord(self.r_codebox.get(1.0, END))
        else:
            trec = Trecord()
            for table in self.basetable:
                trec.base[table.label] = table.box.get(1.0,END).strip('\n ')
            for table in self.notetable:
                trec.note[table.label] = table.box.get(1.0,END).strip('\n ')
            trec.update()
            self.tlib.addtrecord(trec)
            '''
            if self.currenttitle:
                label = self.tlib.getlabel(self.currenttitle)
            for table in self.basetable:
                self.tlib[label].base[table.label] = table.box.get(1.0,END).strip('\n')
            for table in self.notetable:
                self.tlib[label].note[table.label] = table.box.get(1.0,END).strip('\n')
                '''
        self.updatewindow()
        self.autosave()
    def __loadbibfile(self):
        self.tlib.loadbib(self.filename)
        self.updatethesislistwithtlib()
    def openbibfile(self, msg=None):
        self.filename = filedialog.askopenfilename()
        self.__loadbibfile()
    def savebibfile(self, msg=None):
        filename = filedialog.asksaveasfilename()
        # ask overwrite
        self.tlib.savebib(filename)
    def autosave(self, msg=None):
        try:
            fp = open(self.cachefile, 'wb')
            pickle.dump(self.tlib, fp)
            fp.close()
        except:
            pass
    def autoload(self, msg=None):
        try:
            fp = open(self.cachefile, 'rb')
            self.tlib = pickle.load(fp)
            fp.close()
        except:
            pass
if __name__ == '__main__':
    top = Tk()
    app = Application(top)
    #app.tlib.loadbib('test.bib')
    #app.autoload()
    #app.updatethesislistwithtlib()
    app.mainloop()