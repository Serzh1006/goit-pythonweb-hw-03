from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_html_file("index.html")
        else:
            self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def do_POST(self):
        print(self.path)


server = HTTPServer(("", 3000), HttpHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
