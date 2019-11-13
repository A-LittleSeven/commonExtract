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

    def cut(self, node):
        del node
        return 0

    def __str__(self):
        return "pre:{}, ele:{}, nlevel:{}"\
            .format(self.pre, self.elem, self.nlevel)


class commonExtractor():

    def __init__(self, debug=1, image=False, thres=20):
        
        self.DUBUG = debug
        self.IMAGE = image
        # TODO: 对标签内文字做阈值处理
        self.THRES = thres
        self.definite = ("p", "blockquote")
        self.containor = None

    def readUrl(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        try:
            res = requests.get(self.url, headers=header)
            content = res.text
            return content
        except Exception as e:
            print(e)

    #  preprocess the dom tree
    def processUseless(self, elem_tree):
        ignore = ("header", "footer", "script",
                  "style", "a", "form", "nav", "head")
        for child in elem_tree.getchildren():
            if child.tag in ignore or type(child) == _Comment:
                child.getparent().remove(child)
            self.processUseless(child)
        return elem_tree
    
    def processImgs(self, content):
        reIMG = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
        content = reIMG.sub(r'{\1}', content)
        return content
        
    def ContentSpliter(self, ghtml): 
        tree = self.processUseless(etree.HTML(ghtml))
        # recursively get child element
        self.cutNode(Node(None, tree, 1) ,tree)
        elemContent = etree.tostring(self.containor.elem, encoding=str)
        Hcontent = str(elemContent)
        if self.IMAGE:
            Hcontent = self.processImgs(Hcontent)
        reTAG = r'<[\s\S]*?>|[ \t\r\f\v]|&#13;|&gt;'
        filterdContent = re.sub(reTAG, "", Hcontent)
        mainContent = "".join(re.findall("\s\S+", filterdContent))
        if self.DUBUG:
            print(mainContent)
            with open("mainContent.txt", 'w') as f:
                f.write(mainContent)
        return mainContent

    # define the search rule
    def dynamicfind(self, node, child, nlevel):
        if child.tag in self.definite:
            self.findancestor(node)
            return False
        else: return True

    def cutNode(self, node, elem_tree, nlevel = 2):
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
            else: node = node.pre
            return self.findancestor(node)

    @staticmethod
    def readFromFile(filePath):
        with open(filePath, encoding="utf-8") as hfp:
            content = hfp.read()
        return content


if __name__ == "__main__":
    
    # http://www.sohu.com/a/353449767_267106?g=0%253Fcode=a315343389f3a899c29ceaed4215ceb0&spm=smpc.home.top-news1.1.1573626200338DhoZ4ic&_f=index_cpc_0
    t = commonExtractor(debug=1, image=True)
    ghtml = t.readFromUrl(
        "https://www.zybuluo.com/Alston/note/778377")
    # ghtml = t.readFromFile("testDynamic.html")
    t.ContentSpliter(ghtml)
