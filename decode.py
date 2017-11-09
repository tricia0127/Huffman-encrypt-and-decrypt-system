#!/usr/bin/python
# -*- coding: utf-8 -*-
import random,os

class Decode:
    def __init__(self, fr):
        self.fr = fr
        #self.name = new.fileName1
       # self.fr = open("/Users/zhangchuyue/Desktop/B15040805张楚月_哈夫曼加解密工具/password dictionary/"
        #               + self.name, 'r', encoding='utf-8', errors='ignore')


 #从文件中读取下一个节点的信息
    def __readNextNode(self):
        node = self.fr.readline().strip('\n')
        if node == '':
            self.fr.close()
            return None
        return node.split(':')

    #返回文件中所有节点信息构成的列表
    def getNodes(self):
        nodes = []
        node = self.__readNextNode()
        while node != None:
            nodes.append(node)
            node = self.__readNextNode()
        return nodes

    # 将所有节点信息构成的列表存入文件
    def saveNodes(self, nodes):
        fw = open(self.fileName, 'w')
        for node in nodes:
            string = node[0] + ':' + node[1] + '\n'
            fw.write(string)
        fw.close()

if __name__ == '__main__':
    new = Decode()
    print (new.getNodes())