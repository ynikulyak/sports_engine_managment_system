#!/usr/bin/env python3 

# This file must be in the /cgi-bin/ directory of the server.
import cgitb, cgi, sports, sportslib

# Enable CGI errors and extract arguments
cgitb.enable()
arguments = cgi.FieldStorage()

# Filnames for header and footer
header_filename = "_header.html"
footer_filename = "_footer.html"
admin_menu_filename = "admin/_admin_menu.html"

# Determine the action and body file to open from the index directory
action = sportslib.sanitize_file_name(arguments.getvalue("action", "home"))
action_file = action + ".html"
# Admin action templates are withoud "admin_" prefix in admin directory.
action_file = action_file.replace("admin_", "admin/")

# Read cookies
cookies = sportslib.get_cookies()

# Start main web applicatiom action to get dynamic contents for body
app = sports.Application(action, arguments, cookies)
application_result = app.start()

# Test if there cookies to set (must set it before content type header).
if ("cookies" in application_result.keys()):
    sportslib.set_cookies(application_result['cookies'])

# Send HTML and UTF-8 headers.
print("Content-Type: text/html; charset=utf-8")
print()

if ("location" in application_result.keys()):
	# Process redirect
	print(sportslib.redirect(application_result['location']))
else:
	# Send HTML header 
	header_template = sportslib.file_get_contents('./' + header_filename)
	print(sportslib.build_template(header_template, application_result))

	if sportslib.get_logged_in_user_id() and action.startswith("admin_"):
	   admin_menu_template = sportslib.file_get_contents('./' + admin_menu_filename)
	   print(sportslib.build_template(admin_menu_template, application_result))

	# Send HTML body
	body_file_template = sportslib.file_get_contents('./' + action_file)
	print(sportslib.build_template(body_file_template, application_result))

	# Send HTML footer
	footer_template = sportslib.file_get_contents('./' + footer_filename)
	print(sportslib.build_template(footer_template, application_result))
