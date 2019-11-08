# coding:utf-8

# __author__ = meow
# meow meow meow~

from lxml import etree
from lxml.etree import _Comment
from bs4 import BeautifulSoup
import re
import requests

# store the prefix
class Node():
    def __init__(self, pre0, ele0, nlevel):
        self.pre = pre0
        self.ele = ele0
        self.nlevel = nlevel

    def __str__(self):
        return "pre:{}, ele:{}, nlevel:{}".format(self.pre, self.ele, self.nlevel)


class commonExtractor():

    def __init__(self, mode='definite', thres=1, debug=0):
        
        self.MODE = mode
        self.THRES = thres
        self.DUBUG = 1
        # define the ignored tag in html
        self.igonre = ("header", "footer", "script", "style", "a")
        self.ignoreComment = type(_Comment)
        # definr the text containor tags
        self.definite = ("p", "article", "h")
        self.likelihood = self.definite  + ("ul", "table", "h1")
        self.ele_splitList = []

    def ContentSpliter(self, ghtml):

        ele_parser = []
        soup = BeautifulSoup(ghtml, "html.parser")
        # find the main content of a html
        mainContent = soup.find("body")
        # prettify the input html
        prettydContent = mainContent.prettify(encoding="utf-8")
        tree = etree.HTML(prettydContent)
        # recursively get child element
        self.cutNode(Node(None, tree, 1) ,tree)
        if self.DUBUG: print(self.ele_splitList)
        # div = self.miniTree
        # content = div.toString()
        
        
    # filter the useless tag
    def filter(self, node, child, nlevel):
        if child.tag in self.igonre:
            return False
        if type(child) == _Comment:
            return False
        if child.tag in self.definite:
            self.ele_splitList.append(Node(node, child, nlevel))
            return False
        else:
            return True

    def cutNode(self, node, elem_tree, nlevel = 2):
        prenode = node
        if elem_tree == []:
            return
        for child in elem_tree.getchildren():
            if self.filter(prenode, child, nlevel):
                node = Node(prenode, child, nlevel)
                self.ele_splitList.append(node)
                self.cutNode(node, child, nlevel * 2)
            else:
                continue
    
    def findancestor(self):
        pass

    @staticmethod
    def readFromUrl(url):
        pass

    @staticmethod
    def readFromFile(filePath):
        with open(filePath, encoding="utf-8") as hfp:
            content = hfp.read()
        return content


if __name__ == "__main__":

    # print(_Comment)
    t = commonExtractor(debug=0)
    ghtml = t.readFromFile("baidu.html")
    t.ContentSpliter(ghtml)

    
