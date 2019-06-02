def genHTMLWithBody(bodyTxt):
    strH = '''<!DOCTYPE html>
    <html>
        <head>  
            <style> 
            table { 
            border-collapse: collapse;
            }

            table, td, th {
            border: 1px solid black;
            }
            </style>
        </head> 
    <body>'''
    strT = '''
    </body>
    </html>'''
    return strH + bodyTxt + strT

def tableOf(rowTxt):
    return '<table>\n' + rowTxt + '\n</table>\n'

def rowOf(colTxt):
    return '<tr>' + colTxt + '</tr>\n'

def headerColOf(colTxt):
    return '<th>' + colTxt + '</th>\n'

def headerRowFromList(listelems):
    col = ''
    for ele in listelems:
        col = col + headerColOf(ele)
    return rowOf(col)

def colOf(valTxt, rowspan = 0):
    if rowspan == 0:
        return '<td>' + valTxt + '</td>'
    else:
        return '<td rowspan=%s>\n'%str(rowspan) + valTxt + '\n</td>' 
