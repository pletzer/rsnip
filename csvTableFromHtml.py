#!/usr/bin/env python

from __future__ import print_function

import urllib2
from bs4 import BeautifulSoup
import re

class CsvTableFromHtml:

    def __init__(self, url):
        self.soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
        self.tables = []
        self.tableNames = []
        
    def findTables(self, className="wikitable sortable"):
        tables = self.soup.find_all('table', attrs={"class": className})
        for index in range(len(tables)):
            table = tables[index]
            all_headers = table.find_all("th")
            dataset = []
            dataName = self.__removeSpaces( \
                         self.__removeComma( \
                           self.__removeDot(all_headers[0].get_text()) \
                                           ) \
                                          )
            if dataName:
                self.tableNames.append(dataName)
            else:
                self.tableNames.append('table{}'.format(index))
            # get column headers
            headers = []
            for th in all_headers[1:]:
                header = th.get_text()
                if header and header != "u''":
                    headers.append(self.__removeEmpty(self.__removeComma(header)))
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
            print(self.__filter(line))
        
    def saveTableToCSV(self, index):
        f = open(self.tableNames[index] + '.csv', 'w')
        for row in self.tables[index]:
            line = ''
            for val in row:
                line += val + ','
            print(self.__filter(line).encode('utf-8'), file=f)
            
    def __filter(self, line):
        # replace two consecutive commas with ,NA,
        newLine = line[:]
        #newLine = re.sub(r'\,\s*\,', ',NA,', line)
        # remove trailing comma
        newLine = re.sub(r'\,\s*$', '', newLine)
        return newLine
        
    def __removeComma(self, line):
        return re.sub(r'\n', ' ', re.sub(r"\,", " or ", line))
        
    def __removeDot(self, line):
        return re.sub(r'\.', ' ', line)
            
    def __removeSpaces(self, line):
        return re.sub(r'\s', '_', line)
        
    def __removeEmpty(self, line):
        return re.sub(r"u''", "", line)
        
#############################################################################
def test():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate'
    page = CsvTableFromHtml(url)
    page.findTables()
    #page.printTable(2)
    for ti in range(page.getNumberOfTables()):
        page.saveTableToCSV(2)
    
if __name__ == '__main__': test()
        
    
