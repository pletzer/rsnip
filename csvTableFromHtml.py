#!/usr/bin/env python

from __future__ import print_function

import urllib2
from bs4 import BeautifulSoup
import re

class CsvTableFromHtml:

    def __init__(self, url):
        self.soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
        self.tables = []
        
    def findTables(self, className="wikitable sortable"):
        tables = self.soup.find_all('table', attrs={"class": className})
        for table in tables:
            dataset = []
            # get the headers
            headers = [th.get_text() for th in table.find("tr").find_all("th")]
            if headers:
        	    dataset.append(headers)
            # get the data 
            for row in table.find_all("tr")[1:]:
                datarow = [td.get_text() for td in row.find_all("td")]
                if datarow:
            	    dataset.append(datarow)
            self.tables.append(dataset)
        
    def getNumberOfTables(self):
        return len(self.tables)
        
    def printTable(self, index):
        for row in self.tables[index]:
            line = ''
            for val in row:
                line += val + ','
            print(re.sub(r'\,\s*$', '', re.sub(r'\,\s*\,', ',NA,', line)))
        
    def saveTableToCSV(self, filename, index):
        f = open(filename, 'w')
        for row in self.tables[index]:
            line = ''
            for val in row:
                line += val + ','
            line = re.sub(r'\,\s*$', '', re.sub(r'\,\s*\,', ',NA,', line))
            print(line.encode('utf-8'), file=f)
        
#############################################################################
def test():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate'
    page = CsvTableFromHtml(url)
    page.findTables()
    page.printTable(2)
    for ti in range(page.getNumberOfTables()):
        page.saveTableToCSV('table{}.csv'.format(ti), 2)
    
if __name__ == '__main__': test()
        
    
