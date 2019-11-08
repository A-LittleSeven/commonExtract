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
    def __init__(self, prefix, element, nlevel):
        self.pre = prefix
        self.elem = element
        self.nlevel = nlevel

    def __str__(self):
        return "pre:{}, ele:{}, nlevel:{}"\
            .format(self.pre, self.elem, self.nlevel)


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
        self.elemTmpList = []
        self.containor = None
        

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
        if self.DUBUG: print(etree.tostring(self.containor.elem))



    # define the stop rules
    def filter(self, node, child, nlevel):
        if child.tag in self.igonre: return False
        if type(child) == _Comment: return False
        if child.tag in self.definite:
            self.findancestor(node)
            # self.elemTmpList.append(Node(node, child, nlevel))
            return False
        else: return True


    def cutNode(self,  node , elem_tree, nlevel = 2):
        prenode = node
        if elem_tree == []:
            return
        for child in elem_tree.getchildren():
            if self.filter(prenode, child, nlevel):
                node = Node(prenode, child, nlevel)
                self.elemTmpList.append(node)
                self.cutNode(node, child, nlevel * 2)
            else:
                continue
    
    def findancestor(self, node):
        if self.containor == None:
            self.containor = node.pre
        elif node.pre == self.containor:
            return
        else:
            self.containor = self.containor.pre
            return self.findancestor(node)
        

    @staticmethod
    def readFromUrl(url):
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        res = requests.get(url, headers=header)
        res.encoding = res.apparent_encoding
        content = res.content
        return content

    @staticmethod
    def readFromFile(filePath):
        with open(filePath, encoding="utf-8") as hfp:
            content = hfp.read()
        return content


if __name__ == "__main__":

    # print(_Comment)
    t = commonExtractor(debug=1)
    ghtml = t.readFromUrl("https://www.cnblogs.com/xieqiankun/p/generalnewsextractor.html")
    t.ContentSpliter(ghtml)
