#!/usr/bin/python3

import json
import http.server
import socketserver

class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            length = int(self.headers['content-length'])
            form = json.loads(self.rfile.read(length).decode('utf-8'))
            print(form)
            if self.path == '/new_game':
                response = self.new_game(form)
            self.send_response(200)
            self.end_headers()
            if response:
                self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path not in ['/background.jpg']:
            self.path = '/index.html'
        with open('httpd' + self.path, 'rb') as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

    def new_game(self, form):
        form['new_game_name'] = 'got it ' + str(id(form))
        return form

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Httpd) as httpd:
    httpd.serve_forever()
