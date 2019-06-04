def genHTMLWithBody(bodyTxt):
    strH = '''<!DOCTYPE html>
    <html>
        <head>  
            <style> 
                #customers {
                font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
                }

                #customers td, #customers th {
                border: 1px solid #ddd;
                padding: 8px;
                }

                #customers tr:nth-child(even){background-color: #f2f2f2;}

                #customers tr:hover {background-color: #ddd;}

                #customers th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: #4CAF50;
                color: white;
                }
            </style>
        </head> 
    <body>'''
    strT = '''
    </body>
    </html>'''
    return strH + bodyTxt + strT

def tableOf(rowTxt, id='customers'):
    return '<table id=%s>\n'%id + rowTxt + '\n</table>\n'

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

def rowFromList(listelems):
    col = ''
    for ele in listelems:
        col = col + colOf(ele)
    return rowOf(col)