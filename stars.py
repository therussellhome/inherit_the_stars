#!/usr/bin/python3

import json
import http.server
import socketserver

def range_check(form, ranges):
    values = {}
    for name in ranges:
        default = ranges[name]
        try:
            value = form[name]
            if type(default[0]) == int:
                value = max([default[1], min([default[2], int(value)])])
            elif type(default[0]) == float:
                value = max([default[1], min([default[2], float(value)])])
            elif type(default[0]) == bool:
                value = bool(value)
            elif type(default[0]) == type(value):
                pass
            else:
                value = default[0]
        except:
            value = default[0]
        values[name] = value
    return values

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
        ranges = {
            'new_game_name': [''],
            'new_game_x': [100, 1, 100], 
            'new_game_y': [100, 1, 100], 
            'new_game_z': [100, 1, 100], 
            'new_game_density': [95, 1, 100],
            'new_game_number_of_players': [1, 1, 16],
            'new_game_player_distance': [15, 1, 50],
            'new_game_public_player_scores': ['yes'], 
            'new_game_victory_tech': ['on'],
            'new_game_victory_tech_level': [20, 1, 50], 
            'new_game_victory_tech_level_in_fields': [4, 1, 6], 
            'new_game_number_of_ships': [300, 1, 500], 
            'new_game_number_of_planets': [75, 1, 200], 
            'new_game_number_of_factories': [200, 1, 500], 
            'new_game_number_of_power_plants': [200, 1, 500], 
            'new_game_number_of_mines': [200, 1, 500], 
            'new_game_number_of_other_players_left': [0, 0, 15], 
            'new_game_number_of_conditions_met': [1, 1, 9], 
            'new_game_years_till': [75, 1, 200], 
        }
        return range_check(form, ranges)

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Httpd) as httpd:
    httpd.serve_forever()
