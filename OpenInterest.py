
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
    firsttable = soup.find_all('table')[0] 
    bText = firsttable.find_all('tr')[0].find('b').text
    bL =  bText.split(' ')
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
    return (bL[1], rowstrs)

def openIsOfScrips(datee, scrips):
    scriptDic = {}
    cVals = []
    for scrip in scrips:
    #for scrip in [nifty50Scrips[0], nifty50Scrips[1]]:
        print("=============================================")
        print("Generating for Scrip : %s" % scrip)
        print("=============================================")
        cVal, scriptDic[scrip]= printOIPerScrip(scrip, datee)
        cVals.append(cVal)
    return cVals,scriptDic

def openIsOfNifty50(datee):
    nifty50Scrips = getNifty50Scrips()
    return openIsOfScrips(datee, nifty50Scrips)

def genHTMLTableForOIs(cVals, oiDict, filePath):
    rowHeaders = ['OI', 'IV', 'LTP', 'Strike Price', 'Strike Price', 'LTP',	'IV', 'OI']
    rowsTxt = ''
    callOrPut = [1, 21] # 1 and 21 are the open interest values OI
    for eachKey,cVal in zip(oiDict, cVals):
        rowsTxt = rowsTxt + headerRowFromList([eachKey, cVal, '', 'call', 'put', '', '', '']) 
        rowsTxt = rowsTxt + headerRowFromList(rowHeaders)
        tableOfOIs = oiDict[eachKey]        
        colTxt = ''
        tableOfOIs.sort(key = lambda x: float(x[callOrPut[0]]))
        #callTab = copy.deepcopy(tableOfOIs[-4:-1])
        callTab = tableOfOIs[-4:-1]        
        tableOfOIs.sort(key = lambda x: float(x[callOrPut[1]]))
        #optionsTab = copy.deepcopy(tableOfOIs[-4:-1])
        optionsTab = tableOfOIs[-4:-1]

        for i in range(0,3):
            #rowstrs[-4][1], rowstrs[-4][4], rowstrs[-4][5], rowstrs[-4][11]
            #Call data
            OI = currutils.genComma(callTab[i][1])
            colTxt = colTxt + colOf(str(OI))
            colTxt = colTxt + colOf(callTab[i][4])
            colTxt = colTxt + colOf(callTab[i][5])
            colTxt = colTxt + colOf(callTab[i][11])
            #Put data
            colTxt = colTxt + colOf(optionsTab[i][11])
            colTxt = colTxt + colOf(optionsTab[i][17])
            colTxt = colTxt + colOf(optionsTab[i][18])
            OIP = currutils.genComma(optionsTab[i][21])
            colTxt = colTxt + colOf(OIP)
            rowsTxt = rowsTxt + rowOf(colTxt)
            colTxt = '' # clear next col
    htmltxt = genHTMLWithBody(tableOf(rowsTxt))
    fileutils.writeStrToFile(htmltxt, filePath)

def genOIsHTMLForNifty50(datee, filePath):
    cVals, oiDict = openIsOfNifty50(datee)
    genHTMLTableForOIs(cVals, oiDict, filePath)

def genOIsHTMLForScrips(datee, scrips, filePath):
    cVals, oiDict = openIsOfScrips(datee, scrips)
    genHTMLTableForOIs(cVals, oiDict, filePath)
        
#openIs("27JUN2019")
#openIs(sys.argv[1])

#genOIsHTMLForNifty50("27JUN2019", 'C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\manga.html')
genOIsHTMLForScrips("27JUN2019", ['IOC', 'TATAMOTORS'], 'C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\manga.html')


#printOIPerScrip('M&M', '27JUN2019')
#nifty50Scrips = getNifty50Scrips()
#print (nifty50Scrips)


















#https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTSTK&symbol=TCS&date=27JUN2019

#https://www.nseindia.com/content/indices/ind_nifty50list.csv

#nifty50Links = getNifty50Links()
#https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=SBIN
#print (nifty50Links[30])
#print(soup.prettify())