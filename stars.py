#!/usr/bin/python3

import http.server
import re
import socket
import socketserver
import urllib.parse
import webbrowser
from pathlib import Path
from stars import *


""" Map of post handlers """
_handlers = {
    '/launch': launch.Launch(),
    '/new_game': new_game.NewGame(),
    '/launch': launch.Launch(),
    '/race_editor': race_editor.RaceEditor(),
    '/tech': tech_display.TechDisplay(),
}


class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            form, action = [self.path, '']
            if '?' in self.path:
                form, action = self.path.split('?')
                action = urllib.parse.unquote(action)
            length = int(self.headers['content-length'])
            json = game_engine.from_json(self.rfile.read(length).decode('utf-8'))
            response = _handlers.get(form, None)
            self.send_response(200)
            self.end_headers()
            print('    post = ', json)
            if response:
                _handlers[form].update(**json)
                _handlers[form].post(action)
                response_str = game_engine.to_json(response)
                print('    resp = ', response_str)
                self.wfile.write(response_str.encode())

    def do_GET(self):
        get = Path('.') / 'www' / re.sub('\?.*', '', self.path).split('/')[-1]
        if not get.exists() or get.is_dir():
            get = Path('.') / 'www' / 'index.html'
        with open(get, 'rb') as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

with socketserver.TCPServer(("", 0), Httpd) as httpd:
    address = 'http://' + socket.gethostname() + ':' + str(httpd.server_address[1])
    print('Connecting to', address)
    webbrowser.open(address)
    httpd.serve_forever()
