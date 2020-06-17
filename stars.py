#!/usr/bin/python3

import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path
from stars import *


""" Map of post handlers """
_handlers = {
    '/launch': launch.Launch(),
    '/new_game': new_game.NewGame(),
    '/launch': launch.Launch(),
    '/race_editor': race_editor.RaceEditor()
}


class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            form, action = [self.path, '']
            if '?' in self.path:
                form, action = self.path.split('?')
            length = int(self.headers['content-length'])
            json = game_engine.from_json(self.rfile.read(length).decode('utf-8'))
            print('-----------------------------------')
            print('    post = ', json)
            response = _handlers.get(form, None)
            self.send_response(200)
            self.end_headers()
            if response:
                _handlers[form].update(**json)
                _handlers[form].post(action)
                response_str = game_engine.to_json(response)
                print('    resp = ', response_str)
                self.wfile.write(response_str.encode())
            print('-----------------------------------')

    def do_GET(self):
        get = Path('.') / 'www' / self.path.split('/')[-1]
        print(get)
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
