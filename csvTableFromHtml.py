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
            dataset = []
            startIndex = 0
            tableField = table.find('th', attrs={'colspan': re.compile(r'\d+')})
            if tableField:
                tableName = tableField.get_text()
                tableName = self.__removeSpaces(self.__removeComma(self.__removeDot(tableName)))
                self.tableNames.append(tableName)
                startIndex = 1
            else:
                self.tableNames.append('table{}'.format(index))
            # get column headers
            headers = []
            all_headers = table.find_all("th")
            for th in all_headers[startIndex:]:
                header = th.get_text()
                if header and header != "u''":
                    # remove funny character
                    header = re.sub(r'^[^\w]+', '', header)
                    headers.append(self.__removeEmpty(self.__removeComma(header)))
            dataset.append(headers)
            # get the data 
            for row in table.find_all("tr")[startIndex:]:
                datarow = [re.sub(r'\,', '', td.get_text()) for td in row.find_all("td")]
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
        # remove reference
        newLine = re.sub(r'\[\d+\]', '', newLine)
        # remove funny leading characters
        newLine = re.sub(r'^[^\w]+', '', newLine)
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
def getHomicideData():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate'
    page = CsvTableFromHtml(url)
    page.findTables()
    #page.printTable(2)
    for ti in range(page.getNumberOfTables()):
        page.saveTableToCSV(ti)
        
def getGunData():
    url = 'https://en.wikipedia.org/wiki/Number_of_guns_per_capita_by_country'
    page = CsvTableFromHtml(url)
    page.findTables()
    #page.printTable(0)
    for ti in range(page.getNumberOfTables()):
        page.saveTableToCSV(ti)
    
if __name__ == '__main__': 
    #getHomicideData()
    getGunData()
        
    
