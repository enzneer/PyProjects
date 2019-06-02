# usage 
# import urlutils
# urlutils.writeToFile
def writeToFile(url, filePath):
    page = requests.get(url)
    file = open(filePath,"w")
    file.writelines(page.text)
    file.close()