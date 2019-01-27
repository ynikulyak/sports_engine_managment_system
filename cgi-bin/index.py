#!/usr/bin/env python3 

# This file must be in the /cgi-bin/ directory of the server.
import cgitb , cgi, sportslib
cgitb.enable()
arguments = cgi.FieldStorage()

# Filnames for header and footer
header_filename = "_header.html"
footer_filename = "_footer.html"

# Determine the action and body file to open from the index directory
action = arguments.getvalue("action", "home")
action_filename = sportslib.sanitize_file_name(action) + ".html"

# Send HTML and UTF-8 headers.
print("Content-Type: text/html; charset=utf-8")
print()

# Send HTML header 
print(sportslib.file_get_contents('./' + header_filename))

# Send HTML body
print(sportslib.file_get_contents('./' + action_filename))

# Send HTML footer
print(sportslib.file_get_contents('./' + footer_filename))
