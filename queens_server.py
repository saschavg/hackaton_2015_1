import SimpleHTTPServer
import SocketServer
from queens import *
import json
import time
import logging


class QueenServer(SocketServer.TCPServer):
    allow_reuse_address = True


class QueenRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        start_time = time.time()
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        req = json.loads(data)

        # interpret request
        in_queens = [ (q['x'],q['y']) for q in req['initial_queens']]
        n = req['max_queens_on_sight']
        r = req['rows']
        c = req['columns']

        # run queens game....
        q = QueensGame(n,r,c, queens=in_queens)
        while True:
            q.populate(5)
            if time.time() - start_time > 1.9 :
                break

        successes = q.find_successes()
        board = successes[-1][1]
        queens = q.get_queens(board)
        #logging.error('n {}'.format(q.n))
        #logging.error(QueensGame.printBitMatrix(board, q.a_boards))

        added_queens = [{"x":q[0], "y":q[1]} for q in queens if q not in in_queens]

        # prep response...
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        # Send the html message
        self.wfile.write( json.dumps({'added_queens':added_queens}) )
        return 1

if __name__ == '__main__':
    httpd = QueenServer(('0.0.0.0', 8080), QueenRequestHandler)
    httpd.serve_forever()
