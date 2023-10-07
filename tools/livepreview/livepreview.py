#!/usr/bin/env python3

import os
import sys
import glob
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8888
SERVER_LOCAL_PATH = Path(__file__).resolve().parent
PREVIEW_TEMPLATE  = os.path.join(SERVER_LOCAL_PATH, 'preview.html')
STATIC_TEMPLATE   = os.path.join(SERVER_LOCAL_PATH, 'shader-static.js')
ANIMATED_TEMPLATE = os.path.join(SERVER_LOCAL_PATH, 'shader-animated.js')

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            file_path = self.path[1:]

            if self.path.endswith('.txt') or self.path.endswith('.html'):
                with open(file_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Content-length', os.path.getsize(file_path))
                    self.end_headers()
                    self.wfile.write(f.read())
                return

            elif self.path.endswith('.txt.static') or self.path.endswith('.txt.animated'):
                js_template = STATIC_TEMPLATE
                if self.path.endswith('.txt.animated'):
                    js_template = ANIMATED_TEMPLATE

                with open(PREVIEW_TEMPLATE, 'rb') as f_preview:
                    f_js_template = open(js_template, 'rb')
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f_preview.read())
                    self.wfile.write(f_js_template.read())

                f_js_template.close()
                return

        except IOError:
            self.send_error(404, f'File Not Found: {self.path}')


# Create the HTTP server and run it
server_url = f'http://127.0.0.1:{PORT}'

# By default serve scripts form livepreview directory
serving_directory = SERVER_LOCAL_PATH

if len(sys.argv) > 1:
    serving_directory = os.getcwd() if sys.argv[1] == '--current' else sys.argv[1]
os.chdir(serving_directory)

print(f"Server path:       {SERVER_LOCAL_PATH}")
print(f"Preview template:  {PREVIEW_TEMPLATE}")
print(f"Static template:   {STATIC_TEMPLATE}")
print(f"Animated template: {ANIMATED_TEMPLATE}")
print(f"Serving from:      {serving_directory}")
print(f"Local server at:   {server_url}")
print("")
for f in glob.glob('*.txt'):
    print(f'{server_url}/{f}.static')
    print(f'{server_url}/{f}.animated')

server = HTTPServer(('', 8888), MyRequestHandler)
server.serve_forever()
