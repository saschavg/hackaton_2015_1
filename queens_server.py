import SimpleHTTPServer
import SocketServer
from queens import *
import json


class QueenServer(SocketServer.TCPServer):
    allow_reuse_address = True


class QueenRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        req = json.loads(data)

        # interpret request
        in_queens = [ (q['x'],q['y']) for q in req['initial_queens']]
        n = req['max_queens_on_sight'] + 1
        r = req['rows']
        c = req['columns']

        # run queens game....
        q = QueensGame(n,r,c, queens=in_queens)
        q.run()
        queens = q.get_results()
        added_queens = [{"x":q[0], "y":q[1]} for q in queens if q not in in_queens]

        # prep response...
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        # Send the html message
        self.wfile.write( json.dumps(added_queens) )
        return 1

if __name__ == '__main__':
    httpd = QueenServer(('0.0.0.0', 8080), QueenRequestHandler)
    httpd.serve_forever()
