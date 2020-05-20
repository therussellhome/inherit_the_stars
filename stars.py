#!/usr/bin/python3

import http.server
import socketserver
from src import *


""" Map of post handlers """
_handlers = {
    '/load_game': load_game.LoadGame()
}


class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            length = int(self.headers['content-length'])
            form = game_engine.from_json(self.rfile.read(length).decode('utf-8'))
            print('-----------------------------------')
            print(form)
            response = _handlers.get(self.path, None)
            self.send_response(200)
            self.end_headers()
            if response:
                _handlers[self.path].post(**form)
                response_str = game_engine.to_json(response)
                print(response_str)
                self.wfile.write(response_str.encode())
            print('-----------------------------------')

    def do_GET(self):
        if self.path not in ['/background.jpg']:
            self.path = '/index.html'
        with open('www' + self.path, 'rb') as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Httpd) as httpd:
    httpd.serve_forever()
