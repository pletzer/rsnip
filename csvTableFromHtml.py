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
                res += val + ','
            res +='\n'
        return res
        
    def __filter(self, line):
    	newLine = line.decode('UTF-8')
    	for s in r'\<td[^\>]*\>', r'\<a[^\>]*\>', r'\<\/a\>', \
                 r'\<\/td\>', r'\\n', r"u''", \
                 r'\<th[^\>]*\>', r'\<\/th\>', r'\<br\>':
        	newLine = re.sub(s, '', newLine)
    	return newLine
            
        
#############################################################################
def test():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate'
    page = CsvTableFromHtml(url)
    page.findTables()
    for tableIndex in range(page.getNumberOfTables()):
    	print 'tableIndex = ', tableIndex
        csvTable = page.convertToCSV(tableIndex)
    	f = open('table{}.csv'.format(tableIndex), 'w')
    	f.write(csvTable.encode('utf-8'))
    
if __name__ == '__main__': test()
        
    