from random import shuffle
import time
import sys

class QueensGame(object):

    def __init__(self, board, max_queens_insight):
        self.board = board
        self.max_queens_insight = max_queens_insight

    def run(self, runs=10, endtime=None):

        def doRun(max_queens):
            self.sweep()

            # evaluate result
            queens = self.board.getQueens()
            if len(queens) > len(max_queens):
                max_queens = [q.position for q in queens]

            # clean up
            for q in queens :
                if q in orig_queens: continue
                q.position = None
            return (max_queens, len(queens))


        max_queens = []
        histo=[]
        # store original given set of queens
        orig_queens = self.board.getQueens()

        run_ctr=0
        if endtime:
            while True:
                max_queens, count = doRun(max_queens)
                histo = updateHisto(histo,count)
                if time.time() > endtime: break
                run_ctr+=1
        else:
            for i in range(runs):
                max_queens, count = doRun(max_queens)
                histo = updateHisto(histo,count)
                run_ctr+=1

        print_histo(histo)
        print 'number of runs : {}'.format(run_ctr)
        for p in max_queens:
            Queen(p)
        return max_queens

    def sweep(self):
        positions = self.board.positions[:]
        shuffle(positions)

        for p in positions:
            if p.queen is None:
                Queen(p)

                invalid_queens = self.validate()
                if invalid_queens:
                    p.queen = None


    def validate(self):

        def red(res,queen):

            queens = res[1]
            invalid = res[0]
            for q in queens:
                if queen.inSight(q):
                    queen.insight_cnt += 1
                    q.insight_cnt += 1
            if queen.insight_cnt> self.max_queens_insight:
                invalid.append(queen)

            return (invalid, queens[1:])

        queens = self.board.getQueens()

        for q in queens:
            q.insight_cnt=0

        invalid, _ = reduce(red, queens,([],queens[1:]))
        return invalid


class Board(object):

    def __init__(self, rows, columns, max_queens_insight=1):
        self.nof_rows = rows
        self.nof_cols = columns
        self.max_queens_insight = max_queens_insight

        self._positions=[]
        self._initPositions()

    def _initPositions(self):
        for r in range(self.nof_rows):
            for c in range(self.nof_cols):
                p = Position(r,c)
                self._positions.append(p)

    @property
    def positions(self):
        return self._positions

    def position(self,row, col):
        return next(p for p in self._positions if p.row == row and p.col==col)

    @property
    def rows(self):
        b = [[ 0 for _ in xrange(self.nof_cols)] for _ in xrange(self.nof_rows)]

        for p in self._positions:
            b[p.row][p.col] = p
        return b

    def getQueens(self):
        return [p.queen for p in self._positions if p.queen ]



    def __str__(self):

        rows = self.rows

        def ft(p):
            o='0'
            if p.queen != None:
                o = '1'
            return '{:2}'.format(o)

        return ('\n'.join([''.join(
            [ft(p) for p in row]
            ) for row in rows ]))


class Position(object):
    _queen = None

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def removeQueen(self):
        self._queen = None

    @property
    def queen(self):
        return self._queen

    @queen.setter
    def queen(self, queen):
        if isinstance(queen, Queen):
            self._queen = queen
            if queen.position is not self:
                self._queen.position = self
        else:
            q = self._queen
            self._queen = None
            if q:
                q.position = None

    def __repr__(self):
        return '{}'.format((self.row, self.col))

    def __del__(self):
        self.queen=None


class Queen(object):
    _position = None

    def __init__(self, position=None):
        self.position=position

    def inSight(self, queen):

        return (queen.position.row == self.position.row) or \
           (queen.position.col == self.position.col) or \
           (abs(queen.position.row - self.position.row) == \
            abs(queen.position.col - self.position.col))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if isinstance(position, Position) :
            self._position = position
            if position.queen is not self:
                self._position.queen = self
        else:
            p = self._position
            self._position=None
            if p:
                p.queen = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.position is not None:
            return 'q {}'.format(self.position)
        else:
            return 'q ()'

    def __del__(self):
        self.position=None






def print_histo(histo):
    for i,h in enumerate(histo):
        if h > 0:
            break;
    i -= 2
    if i < 0: i = 0
    print '\n'
    print '\n'.join([ ('{:<2} |{:>2} | {}').format(j,e, 'x'*e) for j,e in enumerate(histo) if j>=i ])
    print '\n'

def updateHisto(histo, count):
    if len(histo)-1 < count:
        histo+= [0]* (count-len(histo) +1)
    histo[count] += 1
    return histo
