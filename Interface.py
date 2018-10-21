# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 22:43:30 2018

@author: sheeplib
"""

from tkinter import *
from tkinter.ttk import *
from Item import *
#from Procedure import *

class UI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.geometry('800x480')
        self.master.title('bib文献管理器')
        self.basetable = list()
        self.notetable = list()
        #self.master['backgroud']='green'
        self.__createWidgets()
        self.__placeWidgets()
        self.__createEvents()
    class Table(object):
        def __init__(self, top, name, label, width=12, height=2):
            self.top = top
            self.name = name
            self.label = label
            self.frame = Frame(top)
            self.title = Label(self.frame, text = self.name, width=width)
            self.box = Text(self.frame, height=height, wrap=CHAR)
        def pack(self):
            self.title.pack(side=LEFT, expand=NO)
            self.box.pack(side=RIGHT, fill=X, expand=YES)
            self.frame.pack(fill=BOTH, pady=6, padx=6)
    def __createWidgets(self):
        self.top = self.winfo_toplevel()
        self.style = Style()
        # 搜索、列表、及bib操作
        self.lframe = Frame(self.top, borderwidth=1, relief=SUNKEN)
        self.l_searchframe = Frame(self.lframe, height=1)
        self.l_searchbox = Entry(self.l_searchframe)
        self.l_searchbutton = Button(self.l_searchframe, text='搜索', width=4)
        self.l_listframe = Frame(self.lframe)
        self.l_listscroll = Scrollbar(self.l_listframe)
        self.l_listlist = Listbox(self.l_listframe, \
                                  yscrollcommand=self.l_listscroll.set, \
                                  selectmode=SINGLE)
        self.l_buttonframe = Frame(self.lframe, height=1)
        self.l_buttonloadbib = Button(self.l_buttonframe, text='添加bib')
        self.l_buttonsavebib = Button(self.l_buttonframe, text='导出bib')
        # 文章具体信息框
        self.rframe = Frame(self.top)
        self.r_tab = Notebook(self.rframe)
        self.r_baseframe = Frame(self.r_tab)
        #self.r_basetest = Button(self.r_baseframe, text='标签1', width=4)##
        self.r_noteframe = Frame(self.r_tab)
        #self.r_notetest = Button(self.r_noteframe, text='标签2', width=4)##
        #self.tabletest = UI.Table(self.r_baseframe, '测试表格单元')##
        for row in tbasetemplate:self.basetable.append(UI.Table(self.r_baseframe, row['中文名']+' ('+row['英文名']+')', row['中文名'], height=row['内容高度']))
        self.r_buttonframe = Frame(self.rframe)
        self.r_buttoncreate = Button(self.r_buttonframe, text='新记录')
        self.r_buttonmodify = Button(self.r_buttonframe, text='保存修改')
        self.r_buttonreflash = Button(self.r_buttonframe, text='刷新')
        for row in tnotetemplate:self.notetable.append(UI.Table(self.r_noteframe, row['中文名']+' ('+row['英文名']+')', row['中文名'], height=row['内容高度']))
        self.r_codeframe = Frame(self.r_tab)
        #self.r_codescroll = Scrollbar(self.r_codeframe)
        self.r_codebox = Text(self.r_codeframe, wrap=WORD)
        
    def __placeWidgets(self):
        self.lframe.place(relx=.006, rely=.01, relwidth=.370, relheight=0.98)
        #self.l_searchframe.place(relx=.006, rely=.01, relwidth=0.988, relheight=1)
        #self.l_searchbox.place(relx=.0, rely=.0, relwidth=0.8)
        #self.lframe.pack()
        self.l_searchframe.pack(fill=X)
        self.l_searchbox.pack(side=LEFT, fill=X, expand=YES)
        self.l_searchbutton.pack(side=RIGHT, expand=NO)
        self.l_listframe.pack(fill=BOTH, expand=YES)
        self.l_listlist.pack(side=LEFT, fill=BOTH, expand=YES)
        self.l_listscroll.pack(side=RIGHT, fill=Y, expand=NO)
        self.l_buttonframe.pack(fill=X, expand=NO)
        self.l_buttonloadbib.pack(side=LEFT)
        self.l_buttonsavebib.pack(side=LEFT)
        self.rframe.place(relx=.388, rely=.01, relwidth=.606, relheight=0.98)
        self.r_baseframe.pack()
        #self.r_basetest.pack()
        self.r_noteframe.pack()
        for table in self.basetable:table.pack()
        self.r_buttonmodify.pack(side=RIGHT)
        self.r_buttoncreate.pack(side=LEFT)
        self.r_buttonreflash.pack(side=LEFT)
        self.r_buttonframe.pack(side=BOTTOM, fill=X)
        self.r_codebox.pack(side=LEFT, fill=Y, pady=6, padx=6)
        #self.r_codescroll.pack(side=RIGHT, fill=Y)
        self.r_codeframe.place()
        for table in self.notetable:table.pack()
        self.r_tab.add(self.r_baseframe, text='基本信息')
        self.r_tab.add(self.r_noteframe, text='阅读记录')
        self.r_tab.add(self.r_codeframe, text='bib代码')
        self.r_tab.pack(fill=BOTH, expand=YES)
        pass
    
    def __createEvents(self):
        pass
        #self.l_listlist.bind("<Double-Button-1>", lambda x: print('aaa'+str(x)))
        #self.l_listlist.bind("<Double-Button-1>", Callback.thesisselect(self, ))

if __name__ == "__main__":
    top = Tk()
    UI(top).mainloop()
    testnotebook = Notebook(top)

    #print(tbasetemplate)
    