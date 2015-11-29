#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import re

class CsvTableFromHtml:

    def __init__(self, url):
        self.soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
        
    def findTables(self, className="wikitable sortable"):
        self.tables = self.soup.find_all('table', attrs={"class": className})
        
    def getNumberOfTables(self):
        return len(self.tables)
        
    def getTable(self, index):
        return self.tables[index]
        
    def convertToCSV(self, index):
        res = ''
        for row in self.tables[index]:
            for col in row:
                val = self.__filter(repr(col))
                print val
                res += val + ','
            res +='\n'
        return res
        
    def __filter(self, line):
    	res = re.sub(r'\<td[^\>]*\>', '', line)
    	res = re.sub(r'\<a[^\>]*\>', '', res)
    	res = re.sub(r'\<\/a\>', '', res)
    	res = re.sub(r'\<\/td\>', '', res)
    	res = re.sub(r'\\n', '', res)
    	return res
            
        
#############################################################################
def test():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate'
    page = CsvTableFromHtml(url)
    page.findTables()
    csvTable = page.convertToCSV(2)
    print csvTable
    
if __name__ == '__main__': test()
        
    