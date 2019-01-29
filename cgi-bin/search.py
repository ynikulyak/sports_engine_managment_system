# hello.py
# this file must be in the /cgi-bin/ directory of the server
import cgitb , cgi
import mysql.connector
cgitb.enable()
arguments = cgi.FieldStorage()

#Filenames for header and footer
header_filename = "_header.html"
footer_filename = "_footer.html"
#
#  code to get input values goes here
#
players = arguments['query'].value

print("Content-Type: text/html")    # HTML is following
print()                             # blank line required, end of headers

qsql = 'select sports, division, team, player from sportslib where play = %s'  

# connect to database
cnx = mysql.connector.connect(user='root',
                                password='xxxxxxxxx',
                                database='sportslib',
                                host='127.0.0.1')

 
#  code to do SQL goes here
cursor = cnx.cursor()
cursor.execute(qslql, (query))
print('<tabble border = "1"><tr><th>sports</th><th>division</th><th>team</th><th>player</th></tr>')
row = cursor.fetchone()
 
if row is None: 
    # must be first visit, insert row
    
    print('There were no players found.')
    
print("</body></html>")
cnx.commit()
cnx.close()  # close the connection 
