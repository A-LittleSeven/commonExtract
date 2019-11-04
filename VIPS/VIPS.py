# coding:utf-8
from lxml import etree
from bs4 import BeautifulSoup
import re
import requests

class vipsExtractor():

    def __init__(self, deeprecur=3):
        # define the max granularity
       self.deeprecur = deeprecur
    
    
    @staticmethod
    def readRawPage(url):
        try:
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            content = res.content
            return content
        except:
            raise TimeoutError
    
    
    @staticmethod
    def readFromFile(filePath):
        with open(filePath, encoding="utf-8") as hfp:
            content = hfp.read()
        return content

    
    @classmethod
    def ContentSpliter(cls, ghtml):
        max_depth = cls().deeprecur
        ele_parser = []
        soup = BeautifulSoup(ghtml, "html.parser")
        mainContent = soup.find()
        # prettify the input html 
        prettydContent= mainContent.prettify(encoding="utf-8")
        while (max_depth):
            ele_parser.append()
            max_depth -= 1
        
        

if __name__ == "__main__":
    t = vipsExtractor()
    ghtml = t.readFromFile("index.html")
    t.ContentSpliter(ghtml)

    
