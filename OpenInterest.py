
import requests
import urlutils
import fileutils
import currutils
from htmlgenutils import *
import sys
from babel.numbers import format_currency
from bs4 import BeautifulSoup
import html

##def getNifty50Links_old():
##    filePath = "C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\nse.html"
##    url = "https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm"
##    urlutils.writeToFile(url, filePath)
##    #Read
##    fContent = fileutils.readFromFile(filePath)        
##    soup = BeautifulSoup(fContent, 'html.parser')
##    table = soup.find("table", { "id" : "dataTable" })
##    links = table.findAll('a')  
##    linkList = []
##    for link in links:
##        linkList.append(str(link))
##    return linkList

def getNifty50Scrips():
    filePath = "C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\nse.csv"
    url = "https://www.nseindia.com/content/indices/ind_nifty50list.csv"
    urlutils.writeToFile(url, filePath)
    #Read csv
    tab = fileutils.readCSVFile(filePath, ',')   
    scrips = []
    for scrip in tab:
        #print("https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=%s" % scrip[2])
        scrips.append(scrip[2])
    scrips.pop(0) #remove first line
    return scrips
    
def printOIPerScrip(scrip, datee):
    url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTSTK&symbol=%s&date=%s" % (scrip.replace('&', '%26'), datee)
    filePath = "C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\%s_oi.html" % scrip
    urlutils.writeToFile(url, filePath)
    fLines = fileutils.readFromFile(filePath)
    soup = BeautifulSoup(fLines, 'html.parser')
    table = soup.find("table", { "id" : "octable" })
    rows = table.findAll('tr') 
    rowstrs = []
    for row in rows:
        cols = row.findAll('td')    
        if not cols:
            continue
        colstrs = []
        for col in cols:
            # strip comma in 123,456,334  => 123,456,334
            coltxt = col.text.strip().replace(',','')
            if '-' in coltxt:
                colstrs.append('0')
            else:
                colstrs.append(coltxt)
        rowstrs.append(colstrs)
    rowstrs.pop() #remove last row which contain total trades
    return rowstrs

def openIs(datee):
    nifty50Scrips = getNifty50Scrips()
    scriptDic = {}
    for scrip in [nifty50Scrips[0], nifty50Scrips[1]]:
    #for scrip in [nifty50Scrips[0], nifty50Scrips[1]]:
        print("=============================================")
        print("Generating for Scrip : %s" % scrip)
        print("=============================================")
        scriptDic[scrip]= printOIPerScrip(scrip, datee)
    return scriptDic

def genHTMLTableForOIs(oiDict, filePath):
    rowHeaders = ['OI', 'IV', 'LTP', 'Strike Price', 'LTP',	'IV',	'Volume',	'OI']
    rowsTxt = ''
    callOrPut = {1:'call', 21: 'put'}
    for eachKey in oiDict:
        for j in [1,21]:
            rowsTxt = rowsTxt + headerRowFromList([eachKey, callOrPut[j], '', '', '', '', '', '']) 
            rowsTxt = rowsTxt + headerRowFromList(rowHeaders)
            tableOfOIs = oiDict[eachKey]        
            colTxt = ''
            oiDict[eachKey].sort(key = lambda x: float(x[j]))
            for i in range(-4,-1):
                #rowstrs[-4][1], rowstrs[-4][4], rowstrs[-4][5], rowstrs[-4][11]
                OI = currutils.genComma(tableOfOIs[i][1])
                colTxt = colTxt + colOf(str(OI))
                colTxt = colTxt + colOf(tableOfOIs[i][4])
                colTxt = colTxt + colOf(tableOfOIs[i][5])
                colTxt = colTxt + colOf(tableOfOIs[i][11])
                colTxt = colTxt + colOf(tableOfOIs[i][17])
                colTxt = colTxt + colOf(tableOfOIs[i][18])
                colTxt = colTxt + colOf(tableOfOIs[i][19])
                OIP = currutils.genComma(tableOfOIs[i][21])
                colTxt = colTxt + colOf(OIP)
                rowsTxt = rowsTxt + rowOf(colTxt)
                colTxt = '' # clear next col
    htmltxt = genHTMLWithBody(tableOf(rowsTxt))
    fileutils.writeStrToFile(htmltxt, filePath)

def genOIsHTML(datee, filePath):
    oiDict = openIs(datee)
    genHTMLTableForOIs(oiDict, filePath)

        
#openIs("27JUN2019")
#openIs(sys.argv[1])
        
genOIsHTML("27JUN2019", 'C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\manga.html')


#printOIPerScrip('M&M', '27JUN2019')
#nifty50Scrips = getNifty50Scrips()
#print (nifty50Scrips)


















#https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTSTK&symbol=TCS&date=27JUN2019

#https://www.nseindia.com/content/indices/ind_nifty50list.csv

#nifty50Links = getNifty50Links()
#https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=SBIN
#print (nifty50Links[30])
#print(soup.prettify())