#!/usr/bin/python3

import http.server
import socket
import socketserver
import tempfile
import webbrowser
from pathlib import Path
from src import *


""" Map of post handlers """
_handlers = {
    '/load_game': load_game.LoadGame(),
    '/launch': launch.Launch()
}


class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            length = int(self.headers['content-length'])
            form = game_engine.from_json(self.rfile.read(length).decode('utf-8'))
            print('-----------------------------------')
            print('    post = ', form)
            response = _handlers.get(self.path, None)
            self.send_response(200)
            self.end_headers()
            if response:
                _handlers[self.path].post(**form)
                response_str = game_engine.to_json(response)
                print('    resp = ', response_str)
                self.wfile.write(response_str.encode())
            print('-----------------------------------')

    def do_GET(self):
        if self.path not in ['/background.jpg', '/favicon.ico']:
            self.path = '/index.html'
        with open('www' + self.path, 'rb') as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

stars_port = Path(tempfile.gettempdir()) / 'stars.port'
if stars_port.exists():
    with open(stars_port) as f:
        address = f.read().strip()
    print('Connecting to', address)
    webbrowser.open(address)
else:
    with socketserver.TCPServer(("", 0), Httpd) as httpd:
        address = 'http://' + socket.gethostname() + ':' + str(httpd.server_address[1])
        try:
            with open(stars_port, 'w') as f:
                f.write(address)
            print('Connecting to', address)
            webbrowser.open(address)
            httpd.serve_forever()
        finally:
            stars_port.unlink(missing_ok=True)
