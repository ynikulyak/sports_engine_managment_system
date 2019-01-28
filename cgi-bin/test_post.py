#!/usr/bin/env python3 

# Test script to test URL arguments, forms and cookies.
# this file must be in the /cgi-bin/ directory of the server
import cgitb, cgi, sportslib
cgitb.enable()
form = cgi.FieldStorage()

print("Content-Type: text/html; charset=utf-8")
print()

print(sportslib.get_cookies())
print(form)