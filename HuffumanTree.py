#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string

sys.setrecursionlimit(1000000)
'''
哈夫曼树节点结构
'''
class TreeNode:
    def __str__(self):
        return '字符=' + repr(self.value) + '-频度=' + repr(self.weight) + '-编码=' + repr(self.encoding)
    def __repr__(self):
        return '字符=' + repr(self.value) + '-频度=' + repr(self.weight) + '-编码=' + repr(self.encoding)

    def __init__(self, lchild = None, rchild = None, value = None, weight = None):
        self.lchild = lchild
        self.rchild = rchild
        self.parent = None
        if self.lchild != None and self.rchild != None:
            self.lchild.parent = self
            self.rchild.parent = self
        self.encoding = ''
        self.value = value
        self.weight = weight


'''   
哈夫曼树
'''
class HuffumanTree:
    def __init__(self,nodeList):
        self.fw = None
        self.encodingList = {}
        nodeList = self.__nodesToObjets(nodeList)
        self.root = self.__createTree(nodeList)
        self.__encode(self.root)
        self.reachAllLeafs(self.root)

    def __nodesToObjets(self, nodeList):
        newList = []
        for node in nodeList:
            obj = TreeNode(value = node[0], weight = int(node[1]))
            newList.append(obj)
        return newList

    #使用给定的节点列表nodeList创建哈夫曼树，返回根节点
    def __createTree(self, nodeList):
        nodeList.sort(key = compare)
        lchild = nodeList[0]
        nodeList.remove(lchild)
        rchild = nodeList[0]
        nodeList.remove(rchild)
        parent = TreeNode(lchild = lchild, rchild = rchild,
                        weight = lchild.weight + rchild.weight)
        if len(nodeList) == 0:
             return parent
        else:
            nodeList.append(parent)
            return self.__createTree(nodeList)


    def display(self, root):
        self.fw = open('tree.txt', 'w')
        self.__display(root)
        self.fw.close()

    #使用缩进格式在文件中输出哈夫曼树
    def __display(self, root, level = ''):
        if level == '':
             self.fw.write(level + repr(root) + '\n')
        else:
            if level[-4] == ' ':
                self.fw.write(level[:-4] + '└───' + repr(root) + '\n')
            else:
                self.fw.write(level[:-3] + '───' + repr(root) + '\n')

        if root.lchild == None:
            return
        self.__display(root. lchild, level + '│   ')
        self.__display(root. rchild, level + '    ')

    #给每个树节点相应的编码值
    def __encode(self, root):
        if root.lchild == None:
            return
        root.lchild.encoding = '0'
        root.rchild.encoding = '1'
        self.__encode(root.lchild)
        self.__encode(root.rchild)

    #获取以nodelist为节点列表的哈夫曼树
    def getTree(self):
        return self.root

    #获取值为value的节点
    def findNode(self, root, value):
        if root.value == value:
            return root
        elif root.lchild == None:
            return None
        else:
            node1 = self.findNode(root.lchild, value)
            node2 = self.findNode(root.rchild, value)
            return node2 if node1 == None else node1

    #从叶子节点node开始，回到跟节点，同时获取该节点的哈夫曼码
    def __goForAncestor(self, node, encoding):
        parent = node.parent
        if parent == None:
            return encoding
        else:
            encoding = self.__goForAncestor(parent, encoding)
            encoding += node.encoding
            return encoding

    #获取字符value的哈夫曼编码
    def getCharEncoding(self, value):
        return self.encodingList[value]

    #获取编码为encoding的字符
    def getCharDecoding(self, encoding):
        return None

    #遍历每个叶子，将每个字符的编码存入字典encodingList
    def reachAllLeafs(self, root):
        if root.lchild == None:
            value = root.value
            encoding = self.__goForAncestor(root, '')
            self.encodingList[value] = encoding
            return
        else:
            self.reachAllLeafs(root.lchild)
            self.reachAllLeafs(root.rchild)


'''
解码/编码器
'''
class Encoding:
    def __init__(self, encodingList):
        self.encodingList = encodingList

    def getStringEncoding(self, string):
        encoding = ''
        while string != '':
            flag = 0
            for (k, v) in self.encodingList.items():
                if string.startswith(k) and string[len(k)] == ' ':
                    encoding += v
                    string = string[len(k) + 1:]
                    flag = 1
                    break
            if flag == 0:
                    raise  Exception
        return encoding

    def getStringDecoding(self, encoding):
        string = ''
        while encoding != '':
            flag = 0
            for (k, v) in  self.encodingList.items():
                if encoding.startswith(v):
                    string += k
                    string += ' '
                    encoding = encoding[len(v):]
                    flag = 1
                    break
            if flag == 0:
                raise Exception
        return string

#设置类TreeNode的比较器
def compare(obj):
    return obj.weight

if __name__ == "__main__":
    from NodeDataIO import *
    io = NodeDataIO()
    nodeList = io.getNodes()
    tree = HuffumanTree(nodeList)
    tree.display(tree.getTree())

