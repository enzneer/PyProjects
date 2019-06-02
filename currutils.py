def genComma(valTxt):
    l = len(valTxt)
    if l < 4: 
        return valTxt
    myList = []
    restTh = (l-3)
    if restTh%2:
        myList.append(valTxt[0])
    for i in range(restTh%2, restTh, 2):
        myList.append('%s%s'%(valTxt[i], valTxt[i+1]))
    myList.append('%s%s%s'%(valTxt[restTh], valTxt[restTh+1],  valTxt[restTh+2]))
    return ','.join(myList)