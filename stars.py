#!/usr/bin/python3

import http.server
import re
import socket
import socketserver
import urllib.parse
import webbrowser
from pathlib import Path
from stars import * # This is needed or json decode will not work correctly
from stars.ui import *


""" Map of post handlers """
_handlers = {
    '/battles': battles.Battles,
    '/drafts': drafts.Drafts,
    '/finance_minister':finance_minister.FinanceMinister,
    '/fleets': fleets.Fleets,
    '/foreign_minister': foreign_minister.ForeignMinister,
    '/host': host.Host,
    '/launch': launch.Launch,
    '/messages': messages.Messages,
    '/new_game': new_game.NewGame,
    '/orders': orders.Orders,
    '/planetary_minister': planetaryministers.PlanetaryMinisters,
    '/planets': planets.Planets,
    '/plans': plans.Plans,
    '/play_complete': play_complete.PlayComplete,
    '/race_editor': race_editor.RaceEditor,
    '/race_viewer': race_viewer.RaceViewer,
    '/render_stars': render_stars.RenderStars,
    '/research_minister': research_minister.ResearchMinister,
    '/score': score.Score,
    '/settings': settings.Settings,
    '/shipyard': shipyard.Shipyard,
    '/tech': tech.Tech,
    '/tech_browser': tech_browser.TechBrowser,
}


class Httpd(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args):
        super().__init__(*args, directory='./www')

    """ Allow override of tech images """
    def do_GET(self):
        if self.path.startswith('/img/'):
            self.directory = game_engine.user_file(self.path[1:], is_www=True)
        super().do_GET()

    """ Call the handler """
    def do_POST(self):
        if self.path == '/shutdown':
            self.server._BaseServer__shutdown_request = True
        else:
            form, action = [self.path, '']
            if '?' in self.path:
                form, action = self.path.split('?')
                action = urllib.parse.unquote(action)
            length = int(self.headers['content-length'])
            post_str = self.rfile.read(length).decode('utf-8')
            json = game_engine.from_json(post_str)
            response = _handlers.get(form, None)
            self.send_response(200)
            self.end_headers()
            #print('    post = ', post_str)
            if response:
                if action == 'reset':
                    if 'player_token' in json:
                        response_str = game_engine.to_json(response(action, player_token=json['player_token']))
                    else:
                        response_str = game_engine.to_json(response(action))
                else:
                    response_str = game_engine.to_json(response(action, **json))
            else:
                response_str = '{}'
            #print('    resp = ', response_str)
            self.wfile.write(response_str.encode())
            game_engine.auto_save()


with socketserver.TCPServer(("", 0), Httpd) as httpd:
    address = 'http://' + socket.gethostname() + ':' + str(httpd.server_address[1])
    print('Connecting to', address)
    webbrowser.open(address)
    httpd.serve_forever()
