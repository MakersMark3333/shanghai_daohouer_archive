
# Library for opening url and creating
# requests
import urllib.request

# pretty-print python data structures
from pprint import pprint

# for parsing all the tables present
# on the website
from html_table_parser.parser import HTMLTableParser

# for converting the parsed data in a
# pandas dataframe
import pandas as pd

import csv, os

class Shanghai_Help_Scraper:

    def __init__(self):
        self.__curr_page = 1
        
        
    # Constructs a URL
    def __url(self, current_page):
        current_page = self.__curr_page
        str1="https://www.daohouer.com/index.php?page="
        str2=str(current_page)
        str3="&hdid=&cjtype=&address="
        url = str1+str2+str3
        return url

    # Opens a website and read its binary contents (HTTP Response Body)
    def __scraper_content(self):
        req = urllib.request.Request(url=self.__url(self.__curr_page))
        f = urllib.request.urlopen(req)
        return f.read()
    
    # Constructing the dataframe
    def __df(self, total_page, upto=-1):
        n = 99999 # i most certainly hope we never reach this number.
        rows = []
        while self.__curr_page <= total_page and n > upto:
            xhtml = self.__scraper_content().decode('utf-8', errors='ignore')
            p = HTMLTableParser()
            p.feed(xhtml)
            title = ['编号', '时间', '程度', '分类', '摘要', '地址', '详情']
            for i in range(1, len(p.tables[0])):
                n = int(p.tables[0][i][0])
                if n <= upto:
                    break
                rows.append(p.tables[0][i])
            print(str(self.__curr_page) + "pages scraped!")
            self.__curr_page += 1
        df = pd.DataFrame(columns = title, data = rows)
        return df
    
    # Function call, users need to provide total_page
    # all=False: only adds new entries on the top; in this case total_page is maximum
    def get(self, total_page, all=False):
        if not all:
            with open("shanghai.csv", "rb") as f:
                f.readline() # discarded
                l = f.readline()
                n = int(l.decode("gbk").split(",")[1])
                df = self.__df(total_page, n)
                df.to_csv('shanghai_new.csv', encoding = 'gbk', errors='ignore')
                with open ("shanghai_new.csv", "ab") as g:
                    while l:
                        g.write(l)
                        l = f.readline()
            os.remove("shanghai.csv")
            os.rename("shanghai_new.csv", "shanghai.csv")
        else:
            df = self.__df(total_page)
            df.to_csv('shanghai.csv', encoding = 'gbk', errors='ignore')

    def pages_scraped(self):
        return self.__curr_page - 1

if __name__ == "__main__":
    test = Shanghai_Help_Scraper()
    test.get(251)
    print("Congratulations, you scraped " + str(test.pages_scraped()) + " pages!!")
