#!/usr/bin/env python3 

# This file must be in the /cgi-bin/ directory of the server.
import appconfig, sportslib, cgitb, cgi, mysql.connector

cgitb.enable()
arguments = cgi.FieldStorage()

#Filenames for header and footer
header_filename = "_header.html"
footer_filename = "_footer.html"
home_filename = "home.html"
#
#  code to get input values goes here
#
query = arguments.getvalue('query', '').replace('%', ' ').strip()

print("Content-Type: text/html; charset=utf-8")    # HTML is following
print()                                            # blank line required, end of headers

result = []
data = {'TABLE_OF_SPORT_DATA': '', 'QUERY': query, 'error': ''}

qsql  = \
'select p.player_first_name, p.player_last_name, p.player_position, \
t.team_name, d.division_name, s.sport_name \
from player p \
left join team_members tm on tm.player_id = p.player_id \
left join team t on t.team_id = tm.team_id \
left join division d on d.division_id = t.division_id \
left join sports s on s.sport_id = t.sport_id \
where p.player_first_name like %s \
or p.player_last_name like %s \
or p.player_position like %s \
or t.team_name like %s \
or d.division_name like %s \
or s.sport_name like %s \
order by p.player_first_name, p.player_last_name'


try:
    # connect to database
    cnx = mysql.connector.connect(
                user=appconfig.database_user,
                password=appconfig.database_password,
                database=appconfig.database_name,
                host=appconfig.database_host)
    #  code to do SQL goes here
    cursor = cnx.cursor()
    if query:
        wild_card = '%' + query + '%'
        cursor.execute(qsql, (wild_card, wild_card, wild_card, wild_card, wild_card, wild_card))
        row = cursor.fetchone()
        while row: 
           result.append((row[0], row[1], row[2], row[3], row[4], row[5]))
           row = cursor.fetchone()
except mysql.connector.Error as err:
    data['error'] = str(err)
finally:
    if cnx:
        cnx.close()  # close the connection 
#print('====<h1>' + str(len(result))  + qsql + '</h1>')
if len(result) > 0:
	table = sportslib.HTMLTable("Player", "Position", "Team", "Division", "Sport")
	for row in result:
		table.add_row(row[0] + ' ' + row[1], row[2], row[3], row[4], row[5])
	data['TABLE_OF_SPORT_DATA'] = table

# Send HTML header 
header_template = sportslib.file_get_contents('./' + header_filename)
print(sportslib.build_template(header_template, data))

# Send HTML body
body_file_template = sportslib.file_get_contents('./' + home_filename)
print(sportslib.build_template(body_file_template, data))

# Send HTML footer
footer_template = sportslib.file_get_contents('./' + footer_filename)
print(sportslib.build_template(footer_template, data))
