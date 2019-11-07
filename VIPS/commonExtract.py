# coding:utf-8

# __author__ = meow
# meow meow meow~

from lxml import etree
from lxml.etree import _Comment
from bs4 import BeautifulSoup
import re
import requests

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
        self.DUBUG = debug
        # define the ignored tag in html
        self.igonre = ("header", "footer", "script", "style", "a")
        self.ignoreComment = type(_Comment)
        # definr the text containor tags
        self.definite = ("p", "article", "h")
        self.likelihood = ("p", "article", "ul", "table", "h1")
        self.ele_splitList = []

    def ContentSpliter(self, ghtml):

        ele_parser = []
        soup = BeautifulSoup(ghtml, "html.parser")
        # find the main content of a html
        mainContent = soup.find("body")
        # prettify the input html
        prettydContent = mainContent.prettify(encoding="utf-8")
        tree = etree.HTML(prettydContent)
        # recursively get child elements
        self.cutNode(tree)
        if self.DUBUG:
            print(self.ele_splitList)

    # filter the useless tag
    def filter(self, elem_tree, child, nlevel):
        if elem_tree.tag in self.igonre:
            return False
        if type(elem_tree) == _Comment:
            return False
        if elem_tree.tag in self.definite:
            self.ele_splitList.append(Node(child, elem_tree, nlevel))
            return False
        else:
            return True

    def cutNode(self, elem_tree, nlevel=1):
        if elem_tree == []:
            return
        for child in elem_tree.getchildren():
            if self.filter(elem_tree, child, nlevel):
                self.ele_splitList.append(Node(elem_tree, child, nlevel))
                self.cutNode(child, nlevel * 2)
            else:
                continue
            
    @staticmethod
    def readFromFile(filePath):
        with open(filePath, encoding="utf-8") as hfp:
            content = hfp.read()
        return content


if __name__ == "__main__":

    # print(_Comment)
    t = commonExtractor(debug=1)
    ghtml = t.readFromFile("baidu.html")
    t.ContentSpliter(ghtml)
    # print(t.ele_splitList)

    
