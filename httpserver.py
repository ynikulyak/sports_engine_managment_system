from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=CGIHTTPRequestHandler):
    port = 8000
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print("server started", port)
    try:
       httpd.serve_forever()
    except:
       pass
    httpd.server_close()
    print("server stopped")

run()
