# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 16:30:13 2018
数据结构
@author: sheeplib
"""
import csv
import copy
import re
import os
import sys
# 载入模板
# fake consts
DICTORDER = 1
# common function
def resource_path(relative_path):
    '''返回资源绝对路径。'''
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
def illegallabel(label):
    return not(legallabel(label))
def legallabel(label):
    return re.match('\w',label)
def extractbypattern(pattern, text):
    result = pattern.search(text)
    if result is None:
        return ''
    else:
        return result.group(1)
def gettemplate(filename):
    csvfile = open(filename,'r')
    csvreader = csv.DictReader(csvfile)
    template = [row for row in csvreader]
    csvfile.close()
    return template
def precompiletemplate(templates):
    for template in templates:
        template['正则表达式'] = re.compile(template['正则表达式'].strip(r'\'"”“'), re.I)
        template['模板'] = template['模板'].strip(r'\'"”“')
tbasetemplate = gettemplate(resource_path('ThesisBaseTemplate.csv')) # 基本信息模板
tnotetemplate = gettemplate(resource_path('ThesisNoteTemplate.csv')) # 笔记模板
precompiletemplate(tbasetemplate)
precompiletemplate(tnotetemplate)
# Items
class anykeydict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self,key) if key in self.keys() else None
class zerodefaultdict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self,key) if key in self.keys() else 0
class Textractor(object):
    def __init__(self, template):
        self.name = 'undefined'
        self.label = ''
        self.template = template # 提取用模板，包含正则表达式
        self.data = anykeydict() # 提取的数据
        self.order = list()
        self.linehead = ''
        self.newlinetag = ''
        for record in self.template:
            self.order.append(record['中文名'])
        self.loaddefault()
    def setlabel(self, label):
        self.label = label
        self['标签'] = label
    def loadbibrecord(self, text): # 通过正则表达式提取单个记录中的数据
        text = text.lstrip()
        for record in self.template:
            tmp = self.decode(extractbypattern(record['正则表达式'], text))
            self.data[record['中文名']] = tmp
        self.name = self.data['标题']
        self.label = self.data['标签']
    def loaddefault(self):
        for record in self.template:
            self.data[record['中文名']] = ''
            self.name = 'default'
            self.label = 'default'
    def recordlist(self): # 列表形式列出记录
        for it in self.data.items():
            yield str(it)
    def __str__(self):
        return '\n'.join(self.recordlist())
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def setlabel(self, label):
        self.data['标签'] = label
        self.label = label
    def _datatocode(self):
        for template in self.template:
            content = self.data[template['中文名']]
            if(content):
                text = self.encode(template['模板'].replace('%replace%',content))
                yield text
        pass
    @property
    def code(self):
        return self.getcode()
        pass
    def getcode(self):
        text ='\n'.join(list(self._datatocode()))
        if(len(text)>8):
            return text + '\n' + self.linehead +'}\n'
        else:
            return ''
        pass
    def decode(self, text):
        if self.linehead:
            text = text.lstrip(self.linehead)
        if self.newlinetag:
            text = text.replace(self.newlinetag, '\n')
        return text
    def encode(self, text): # 一条记录只能占一行
        if self.linehead:
            text = self.linehead + text
        if self.newlinetag:
            text = text.replace('\n', self.newlinetag)
        return text
    def update(self):
        self.label = self.data['标签']
        self.name = self.data['标题']
class Tbase(Textractor):
    # 一篇基本信息记录
    reg = re.compile(r'@article{')
    def __init__(self, label='default'):
        Textractor.__init__(self, tbasetemplate)
        self.setlabel(label)

class Tnote(Textractor):
    # 一篇论文记录
    reg = re.compile(r'%\s*article{')
    def __init__(self, label='default'):
        Textractor.__init__(self, tnotetemplate)
        self.setlabel(label)
        self.linehead = '%'
        self.newlinetag = '<enter>'
class Trecord(object):
    def __init__(self):
        self.base = Tbase()
        self.note = Tnote()
        self.label = None
        self.name = None
        self.preindex = 0
        self.nextindex = 0
    def setlabel(self, label):
        self.label = None
        self.base.setlabel(label)
        self.note.setlabel(label)
    @property
    def code(self):
        return self.base.code + '\n' + self.note.code + '\n'
    def getcode(self):
        return self.code
    def setdefault(self):
        self.base.loadbibrecord('''@article{新建记录, title={请输入标题},}''')
        self.note.loadbibrecord('''%article{新建记录,}''')
        self.update()
        pass
    def loadbibrecord(self, text):
        self.base.loadbibrecord(text)
        self.note.loadbibrecord(text)
        self.update()
    def update(self):
        self.base.update()
        #self.note.update()
        self.label = self.base.label
        self.name = self.base.name
        self.note.setlabel(self.label)
class Tlibrary(object): # 所有论文信息集合，label为唯一key
    def __init__(self):
        self.name = 'undifined'
        self._label2title = anykeydict()
        self._tolabel = anykeydict()
        self._toindex = zerodefaultdict()
        self._data = list()
        self._currentindex = 0
        self._data.append(Trecord())
        self._data[0].setdefault()
        #self._toindex['default'] = 0
        #self.lib = Tlibdict()
    def reset(self):
        del self._data[:]
        self.__init__()
    def addbibrecord(self, text):
        trec = Trecord()
        trec.loadbibrecord(text)
        self.addtrecord(trec)
    def loadbib(self, filename='test.bib'): # 从bib文件中读取数据
        bibreader = openbib(filename)
        record = bibreader.readrecord()
        while(record):
            if Tbase.reg.match(record):
                tbase = Tbase()
                tbase.loadbibrecord(record)
                if legallabel(tbase.label):
                    index = self._autoindex(tbase.label)
                    self._data[index].base = tbase
                    #self._dellabeltitlepair(label=tbase.label, title=tbase['标题'])
                    self._setlabeltitlepair(label=tbase.label, title=tbase['标题'])
            elif Tnote.reg.match(record):
                tnote = Tnote()
                tnote.loadbibrecord(record)
                if legallabel(tbase.label):
                    index = self._autoindex(tnote.label)
                    self._data[index].note = tnote
            record = bibreader.readrecord()
        bibreader.close()
    def savebib(self, filename='save.bib'):
        try:
            fp = open(filename, 'wt', encoding='UTF-8')
            fp.write('% !Mode:: "TeX:UTF-8"\n')
            for index in self._toindex.values():
                fp.write(self._data[index].code)
                #print(record.code)
            fp.close()
        except:
            print('filesaveerror')###############
    def _autoindex(self, label, trecord=None):
        if not(label in self._toindex.keys()):
            if not(trecord):
                trecord = Trecord()
                trecord.setlabel(label)
            self._data.append(trecord)
            self._toindex[label] = len(self._data)-1
        return self._toindex[label]
    def addtrecord(self, trecord):
        if legallabel(trecord.label):
            self._data.append(trecord)
            preindex = self._currentindex
            curindex = len(self._data) - 1
            trecord.preindex = preindex
            if preindex:
                self._data[preindex].nextindex = curindex
            self._toindex[trecord.label] = curindex
            self._dellabeltitlepair(self.curitem.label, self.curitem.name)
            self._setlabeltitlepair(trecord.label, trecord.name)
            self._currentindex = curindex
    def _setlabeltitlepair(self, label, title='Null'):
        self._label2title[label] = title
        self._tolabel[title] = label
        self._tolabel[label] = label
    def _dellabeltitlepair(self, label, title='Null'):
        if self._label2title[label]:
            del self._label2title[label]
        if self._tolabel[title]:
            del self._tolabel[title]
        if self._tolabel[label]:
            del self._tolabel[label]
    def getlabel(self, key): # 将合法输入标签化
        return self._tolabel[key]
    def __getitem__(self, label):
        if label in self._toindex.keys():
            return self._data[self._toindex[label]]
        else:
            return None
    def titlelist(self, order=DICTORDER): # 列出标题
        tlist = list(self._label2title.values())
        if order == DICTORDER:
            tlist.sort()
        else:
            pass
        return tlist
    @property
    def curitem(self):
        return self._data[self._currentindex]
    def select(self, label):
        label = self._tolabel[label]
        if(label):
            self._currentindex = self._toindex[label]
    def selectdefault(self):
        self._currentindex = 0

class Bibfile(object): # 读取bib文件用
    '''
    读取bib文件用
    '''
    objhead=re.compile('@article{|%\s*article{')
    def __init__(self, filestream):
        self.fs = filestream
    def readrecord(self):
        lbracket = 0
        rbracket = 0
        line = self.fs.readline()
        obj = ''
        while line:
            line = line.strip()
            if (self.objhead.match(line) is None) and lbracket<=0:
                line = self.fs.readline()
                continue
            obj += line
            lbracket += len(line.split('{')) - 1
            rbracket += len(line.split('}')) - 1
            if rbracket >= lbracket:
                lbracket = 0
                rbracket = 0
                break
            line = self.fs.readline()
        if len(obj) > 0:
            return obj
        else:
            return None
    def close(self):
        self.fs.close()
        
def openbib(filename):
    try:
        fs = open(filename, 'r', encoding='UTF-8')
        return Bibfile(fs)
    except:
        raise 'File open error'

if __name__ == '__main__':
    #t = Tdata()
    #print(t.base.data)
    sample = '''
% !Mode:: "TeX:UTF-8"
@article{Fu1970Feature,
  title={Feature Selection in Pattern Recognition},
  author={Fu, K. S and Min, P. J and Li, T. J},
  journal={IEEE Transactions on Systems Science and Cybernetics },
  volume={6},
  number={1},
  pages={33-39},
  year={1970},
}
% article{Fu1970Feature} note：总结了特征选择的三个课题：1信息理论方法，2错误率的直接估算，3特征空间变换，4随机自动机模型方法
% article{Fu1970Feature} keyword：特征选择，优化算法，分支决策
    '''
    tt = Tbase()
    tt.loadbibrecord(sample)
#    print(tt.data)
    for it in tt.data.items():
        print(it)
    bibreader = openbib('test.bib')
    record = bibreader.readrecord()
    while(record):
        print(record)
        print('*****************************')
        tt.loadbibrecord(record)
        print(tt)
        print('++++++++++++++++++++++++++++++')
        record = bibreader.readrecord()
    bibreader.close()
    tlib = Tlibrary()
    tlib.loadbib('test.bib')
    #raise(Warning('no key'))
    print('')
    print(tlib.titlelist())
    print(tlib['lb'])
    print(tlib.curitem.base.code+tlib.curitem.note.code)
    #for item in tlib.base.items():
    #    print(item)
    
    