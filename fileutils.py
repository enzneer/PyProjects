# usage 
# import fileutils
# fileutils.readFromFile("c:\rajesh.txt")
def readFromFile(filePath):
    file1 = open(filePath,"r+")
    fContent = file1.readlines()
    file1.close()
    return "\n".join(fContent)

def readCSVFile(filePath, delim):
    file1 = open(filePath,"r+")
    fLines = file1.readlines()
    file1.close()
    table = []
    for line in fLines:
        line = line.rstrip("\n")
        if line:
            rows = line.split(delim)
            table.append(rows)
    return table

def writeStrToFile(str, filePath):
    file = open(filePath,"w")
    file.writelines(str)
    file.close()

