# -*- encoding:utf-8 -*-
__author__ = "meow"

from lxml import etree
from lxml.etree import _Comment
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

    def __init__(self, mode='definite', debug=0):
        
        self.MODE = mode
        self.DUBUG = 1
        # define the ignored tag in html
        self.igonre = ("header", "footer", "script", "style", "a", "form", "nav", "head")
        self.ignoreComment = type(_Comment)
        # definr the text containor tags
        self.definite = ("p","blockquote")
        self.likelihood = self.definite  + ("ul", "table")
        self.elemTmpList = []
        self.containor = None

    #  preprocess the dom tree
    def cutUseless(self, elem_tree):
        for child in elem_tree.getchildren():
            if child.tag in self.igonre or type(child) == _Comment:
                child.getparent().remove(child)
            self.cutUseless(child)
        return elem_tree
        
    def ContentSpliter(self, ghtml):

        ele_parser = []
        tree = self.cutUseless(etree.HTML(ghtml))
        # recursively get child element
        self.cutNode(Node(None, tree, 1) ,tree)
        # if self.DUBUG: print(etree.tostring(self.containor.elem, encoding="utf-8"))
        Hcontent = str(etree.tostring(self.containor.elem, encoding="utf-8"), encoding="utf-8")
        reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'
        filterdContent = re.sub(reTAG, "", Hcontent)
        content = "".join(re.findall("\s\S+", filterdContent))
        if self.DUBUG: print(content)
        with open("dede.txt", 'w') as f:
            f.write(Hcontent)

    # define the search rule
    def dynamicfind(self, node, child, nlevel):
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
            if self.dynamicfind(prenode, child, nlevel):
                node = Node(prenode, child, nlevel)
                # self.elemTmpList.append(node)
                self.cutNode(node, child, nlevel * 2)
            else:
                continue
    
    def findancestor(self, node):
        if self.containor == None:
            self.containor = node.pre
        elif node.pre == self.containor:
            return 0
        else:
            if self.containor.nlevel >= node.nlevel:
                self.containor = self.containor.pre
            else:
                node = node.pre
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
    # ghtml = t.readFromUrl("https://rpy2.readthedocs.io/en/version_2.8.x/robjects_rpackages.html#importing-arbitrary-r-code-as-a-package")
    ghtml = t.readFromFile("testDynamic.html")
    t.ContentSpliter(ghtml)
