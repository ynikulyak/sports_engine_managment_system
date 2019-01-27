import re

def file_get_contents(filename):
  # Reads given file content and returns it as a string
  with open(filename, 'r') as content_file:
    return content_file.read()

def sanitize_file_name(filename):
  # Sanitizes given file name by removing characters 
  # other then a-zA-Z0-9 and _ from the given string.
  return re.sub(r'\W+', '', filename)
