
import requests
import urlutils
import fileutils
import sys
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
def print2console(rowstrs):
    print("=============================================")
    print ("%s-%s-%s-%s" % ("OI", "IV", "LTP", "Strike"))
    for i in range(-4,-1):
        print ("%s-%s-%s-%s" % (rowstrs[i][1], rowstrs[i][4], rowstrs[i][5], rowstrs[i][11]))
    print("=============================================")

def print2html(rowstrs) :
    str = "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (rowstrs[-4][1], rowstrs[-4][4], rowstrs[-4][5], rowstrs[-4][11])
    for i in range(-3,-1):
        str = str + '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(rowstrs[i][1], rowstrs[i][4], rowstrs[i][5], rowstrs[i][11])
    str = str + '</tr>'
    return str

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
        
    rowstrs.sort(key = lambda x: float(x[1]))
    return rowstrs


def openIs(datee):
    nifty50Scrips = getNifty50Scrips()
    scriptDic = {}
    #for scrip in nifty50Scrips:
    for scrip in [nifty50Scrips[0], nifty50Scrips[1], nifty50Scrips[2]]:
        scriptDic(scrip) = printOIPerScrip(scrip, datee)

    str = ''
    for scrip in [nifty50Scrips[0], nifty50Scrips[1], nifty50Scrips[2]]:
        print("=============================================")
        print("Scrip : %s" % scrip)
        print("=============================================")
        str = str + '<tr> <td rowspan="3">%s </td>' % scrip
        col = printOIPerScrip(scrip, datee)
        str = str + col

    strStyle = '''<head>  
                <style> 
                table { 
                border-collapse: collapse;
                }

                table, td, th {
                border: 1px solid black;
                }
                </style>
                </head> '''
    str1 = '<!DOCTYPE html> <html>' + strStyle + '<body> <table> <tr><th><ScripNme></th><th>OI</th><th>IV</th><th>LTP</th><th>Strike Price</th></tr> ' + str + '</table></body> </html>'
    file2 = open("C:\\Users\\Manga\\Documents\\GitHub\\PyProj\\manga.html","w")
    file2.writelines(str1)
    print ("manga.html generated")
    file2.close()

openIs("27JUN2019")
#openIs(sys.argv[1])

#printOIPerScrip('M&M', '27JUN2019')
#nifty50Scrips = getNifty50Scrips()
#print (nifty50Scrips)


















#https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTSTK&symbol=TCS&date=27JUN2019

#https://www.nseindia.com/content/indices/ind_nifty50list.csv

#nifty50Links = getNifty50Links()
#https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=SBIN
#print (nifty50Links[30])
#print(soup.prettify())