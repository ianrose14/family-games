from http.server import BaseHTTPRequestHandler, HTTPServer
import random
from urllib.parse import parse_qs, urlparse

hostName = "localhost"
serverPort = 8080

contentTypeByExt = {
    "html": "text/html",
    "css": "text/css"
}

class GameState():
    def __init__(self, url1, url2):
        self.url1 = url1
        self.url2 = url2

    def nextMove(self):
        pass


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        def w(s):
            self.wfile.write(bytes(s, "utf-8"))

        u = urlparse(self.path)
        qs = parse_qs(u.query)
        
        if u.path == "/":
            self.serveFile("index.html")
            return

        if u.path.endswith(".html") or u.path.endswith(".css") or u.path.endswith(".js"):
            self.serveFile(u.path.removeprefix("/"))
            return
        
        if u.path == "/next":
            print(str(qs))
            print(str(self.server.games))
            gameID = int(qs.get("gameID")[0])
            game = self.server.games.get(gameID)
            if not game:
                w("game %s not found" % gameID)
                return
            
            # TODO

            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server awesome dude.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        form = parse_qs(self.rfile.read(content_length))

        if self.path == "/start":
            gameID = random.randint(1, 1000000)
            self.server.games[gameID] = GameState(form[b"comp1"], form[b"comp2"])
            self.wfile.write(bytes(str(gameID), "utf-8"))
            return


    def serveFile(self, p):
        f = open(p, "r")
        contents = f.read()

        contentType = contentTypeByExt[p.split(".")[-1]]
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()
        self.wfile.write(bytes(contents, "utf-8"))
        return

def main():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    webServer.games = {}
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

main()
