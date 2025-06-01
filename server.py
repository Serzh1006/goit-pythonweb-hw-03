from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
from pathlib import Path
import urllib.parse
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path()


class HttpHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/":
            self.send_html_file("index.html")
        elif self.path == "/message":
            self.send_html_file("message.html")
        elif self.path == '/read':
            self.send_html_file("read.html")
        else:
            filename = BASE_DIR.joinpath(self.path[1:])
            if filename.exists():
                self.send_static(filename)
            else:
                self.send_html_file("error.html", 404)


    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        with open("storage/data.json", "r") as file:
            data_file = json.load(file)
            data_file[str(datetime.now())] = data_dict
        with open("storage/data.json", "w") as file:
            json.dump(data_file, file, indent=4)
        self.generate_html()
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def generate_html(self):
        with open("storage/data.json", "r") as file:
            messages = json.load(file)
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template("read.html")
            output = template.render(messages=messages)
            with open("read.html", "w", encoding='utf-8') as fh:
                fh.write(output)


    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def send_static(self, filename, status=200):
        mt = mimetypes.guess_type(self.path)
        self.send_response(status)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())


server = HTTPServer(("", 3000), HttpHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
