#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter
from HuffumanTree import *
from NodeDataIO import *
import tkinter.messagebox
from tkinter.filedialog import *
import os,sys,re, random

class MyDialog:
    def __init__(self):
        root = Tk()
        root.title('基于哈夫曼算法加解密工具')
        menubar = Menu(root)
        Label(root, text = "这是明文：").grid(row = 0, column = 0)
        Label(root, text = "这是密文：").grid(row = 1, column = 0)
        self.string = Text(root)
        self.encoding = Text(root)
        self.string['width'] = 30
        self.encoding['width'] = 30
        self.string['height'] = 2
        self.encoding['height'] = 8
        self.string.bind('<FocusIn>', self.focusString)
        self.encoding.bind('<FocusIn>', self.focusEncoding)
        self.string.grid(row = 0, column = 1)
        self.encoding.grid(row = 1, column = 1)
        trans = Button(root, text = "随机选一个密码字典，开始转换٩(˃̶͈̀௰˂̶͈́)و", command = self.transform)
        self.__reset = Button(root, text = "重置一下˃̣̣̥᷄⌓˂̣̣̥᷅", command = self.__reset)
        dict = Button(root, text = "生成加密字典库，随机赋权值", command = self.dictionary)
        tree = Button(root, text = "输出树", command = self.printTree)
        getStr = Button(root, text = "从文件导入明文", command = self.getStr)
        getEnc = Button(root, text = "从文件导入密文", command = self.getEnc)
        putStr = Button(root, text = "将解密结果导出到文件", command = self.putStr)
        putEnc = Button(root, text = "将加密结果导出到文件", command = self.putEnc)
        trans.grid(row = 2, column = 2)
        dict.grid(row = 2, column = 0)
        tree.grid(row = 2,column = 1)
        self.__reset.grid(row = 2, column = 3)
        getStr.grid(row = 0, column = 2)
        getEnc.grid(row = 1, column = 2)
        putStr.grid(row = 0, column = 3)
        putEnc.grid(row = 1, column = 3)
        root.mainloop()

    def dictionary(self):
        #os.system("python /Users/zhangchuyue/Desktop/分词+随机权重程序/分词.py")
       f = open("/Users/zhangchuyue/Desktop/分词+随机权重程序/test.txt")
       try:
            text = f.read()  # 读取整个文件并放入一个字符串变量中
            words = re.findall(r"\b[a-zA-Z]{1,50}\b", text)  # 正则匹配所有英文单词得到一个列表
            results = []
            dictionary = {}
            value = 0
            li = [i for i in range(2000)]
            li1 = random.sample(li, 2000)
            for word in words:
                result = word.lower()  # 将英文单词全部转为小写
                results.append(result)
            results = list(set(results))  # 将匹配结果存储在列表里并用set函数去除重复单词
            results.sort()  # 对列表排序
            for result in results:
                dictionary[result] = li1[value]     # 单词为字典的键，随机数为值，作为每个单词的权重
                value += 1
            #number = random.randint(0,1000)
            #output = open("/Users/zhangchuyue/Desktop/B15040805张楚月_哈夫曼加解密工具/password dictionary/dictionary%d.txt" % number, "w")
            output = open("/Users/zhangchuyue/Desktop/B15040805张楚月_哈夫曼加解密工具/password dictionary/dictionary1.txt", "w")
            print(dictionary)
            #print("create password dictionary：" + "dictionary%d.txt" % number)
            for key in dictionary:
                output.writelines(key + ":" + str(dictionary[key]) + "\n")     # 字典内容写入文件
            output.close()
       finally:
            f.close()

    def printTree(self):
        io = NodeDataIO()
        nodeList = io.getNodes()
        tree = HuffumanTree(nodeList)
        tree.display(tree.getTree())
        os.system('notepad tree.txt')

    #字符串导出到文件
    def putStr(self):
        string = self.string.get('0.0', END)
        if string.strip('\n') == '':
                tkinter.messagebox.showwarning("警告", "没有可写的字符")
                return
        fileName = asksaveasfilename()
        if fileName == '':
                return
        fw = open(fileName, 'w')
        fw.write(string)
        fw.close()

    #编码导出到文件
    def putEnc(self):
        encoding = self.encoding.get('0.0', END)
        if encoding.strip('\n') == '':
                tkinter.messagebox.showwarning("警告", "没有可写的字符")
                return
        fileName = asksaveasfilename()
        if fileName == '':
                return
        fw = open(fileName, 'w')
        fw.write(encoding)
        fw.close()

    #从文件中获取字符串
    def getStr(self):
        fileName = askopenfilename()
        if fileName == '':
                return
        fr = open(fileName, 'r')
        string = ''
        tmp = fr.readline().strip('\n')
        while tmp != '':
                string += tmp
                tmp = fr.readline().strip('\n')
        fr.close()
        self.string.delete('0.0', END)
        self.string.insert('0.0', string)
        self.encoding['state'] = 'disabled'

    #从文件中获取编码
    def getEnc(self):
        fileName = askopenfilename()
        if fileName == '':
                return
        fr = open(fileName, 'r')
        string = ''
        tmp = fr.readline().strip('\n')
        while tmp != '':
                string += tmp
                tmp = fr.readline().strip('\n')
        fr.close()
        self.encoding.delete('0.0', END)
        self.encoding.insert('0.0', string)
        self.string['state'] = 'disabled'

    #当字符串文本框获得焦点，将编码框设为不可用
    def focusString(self, event):
        if self.string['state'] == 'normal':
                self.encoding['state'] = 'disabled'

    #当编码框获得焦点，将字符串框设为不可用
    def focusEncoding(self, event):
        if self.encoding['state'] == 'normal':
                self.string['state'] = 'disabled'

    #字符和编码之间相互转化
    def transform(self):
        io = NodeDataIO()
        nodeList = io.getNodes()
        tree = HuffumanTree(nodeList)
        encoder = Encoding(tree.encodingList)
        if(self.encoding['state'] != 'disabled')and(self.string['state'] != 'disabled'):
                return
        elif(self.encoding['state'] == 'disabled')and(self.string['state'] != 'disabled'):
                self.__encode(encoder)
        else:
                self.__decode(encoder)

    #重置所有文本框
    def __reset(self):
        self.string['state'] = 'normal'
        self.encoding['state'] = 'normal'
        self.string.delete('0.0', END)
        self.encoding.delete('0.0', END)
        self.__reset.focus_set()

    #编码
    def __encode(self, encoder):
        text = self.string.get('0.0', END).strip('\n')
        #x = words.split(' ')
        #text = ''.join(x)
        try:
            encoding=encoder.getStringEncoding(text)
        except:
            tkinter.messagebox.showerror('错误', '您输入的文本中包含未编码的字符，请重新输入！')
            return
        self.encoding['state']='normal'
        self.encoding.delete('0.0', END)
        self.encoding.insert('0.0', encoding)
        self.__reset.focus_set()

    #解码
    def __decode(self,encoder):
        text = self.encoding.get('0.0', END).strip('\n')
        try:
            string = encoder.getStringDecoding(text)
        except:
             tkinter.messagebox.showerror('错误', '无法解码，请重新输入!')
             return
        self.string['state'] = 'normal'
        self.string.delete('0.0', END)
        self.string.insert('0.0', string)
        self.__reset.focus_set()

MyDialog()
