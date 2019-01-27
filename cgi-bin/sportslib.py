def file_get_contents(filename):
  with open(filename, 'r') as content_file:
    return content_file.read()
