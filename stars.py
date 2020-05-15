#!/usr/bin/python3

import cgi
import http.server
import socketserver
import urllib

class Httpd(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        print(postvars)
        self.do_GET()

    def do_GET(self):
        if self.path == '/shutdown':
            self.path = '/shutdown.html'
            self.server._BaseServer__shutdown_request = True
        if self.path == '/new_game':
            self.new_game()
        else:
            if self.path not in ['/shutdown.html', '/style.css', '/background.jpg']:
                self.path = '/index.html'
            with open('httpd' + self.path, 'rb') as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())

    def reply(self, title, body):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<html><head><title>')
        if title:
            self.wfile.write(title.encode())
            self.wfile.write(b' - ')
        self.wfile.write(b'Inherit the Stars!</title><link rel="stylesheet" type="text/css" href="style.css">')
        self.wfile.write(b'</head><body>')
        self.wfile.write(b'<a class="home" href="/"><div class="title1">INHERIT THE</div>')
        self.wfile.write(b'<div class="title2">STARS!</div></a>')
        self.wfile.write(b'<a class="shutdown button" href="/shutdown" onclick="if(!confirm(\'Shutdown?\')){return false;}">X</a>')
        self.wfile.write(b'<div class="center"><div>')
        self.wfile.write(body.encode())
        self.wfile.write(b'</div></div></body></html>')

    def new_game(self, **kwargs):
        body = (
'<h1>New Game</h1>'
'<form action="/new_game" method="post"><table>'
'<tr><td>Name</td><td><input type="text" name="name" value="' + kwargs.get('name', '') + '"></td></tr>'
'<tr><td>X</td><td><input type="text" name="size_x" value="' + kwargs.get('size_x', '') + '"></td></tr>'
'<tr><td>Y</td><td><input type="text" name="size_y" value="' + kwargs.get('size_y', '') + '"></td></tr>'
'<tr><td>Z</td><td><input type="text" name="size_z" value="' + kwargs.get('size_z', '') + '"></td></tr>'
'<tr><td colspan="2"><input class="button" type="submit" value="Create Game"></td></tr>'
'</table></form>'
        )
        self.reply('New Game', body)

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Httpd) as httpd:
    httpd.serve_forever()
