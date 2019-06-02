# usage 
# import urlutils
# urlutils.writeToFile
import requests
def writeToFile(url, filePath):
    page = requests.get(url)
    file = open(filePath,"w")
    file.writelines(page.text)
    file.close()
