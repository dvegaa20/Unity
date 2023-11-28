# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import argparse
from src.RappiService import main

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_GET(self):
        data = main()
        json_data = json.dumps(data)
        self._set_response()
        self.wfile.write(json_data.encode('utf-8'))

    def do_POST(self):
        position = {
            "x" : 1,
            "y" : 2,
            "z" : 3
        }

        self._set_response()
        self.wfile.write(str(position).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server to interact with Unity via POST')

    parser.add_argument('-p', '--port', type=int, default=8585, help='Port to run the server on')

    args = parser.parse_args()

    run(port=args.port)