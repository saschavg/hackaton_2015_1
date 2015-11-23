#!/usr/bin/env python
import random
import sys
import ctypes


class QueensGame():

    def __init__(self, n, r, c, queens=[]):
        self.start_queens = queens
        self.n = n+1
        self.l = range(1, self.n)
        self.l.reverse()
        self.size = (r, c)
        self.c = range(c)
        self.r = range(r)
        self.init_validators()
        #self.a_boards = [ [ self.get_rand(3) for _ in xrange(c)] for y in xrange(r)]
        self.a_boards = [ [ 0 for _ in xrange(c)] for y in xrange(r)]

        for q in self.start_queens:
            self.a_boards[q[0]][q[1]] = ~0

        #print 'n = {}'.format(self.n)
        #print 'rows = {}'.format(r)
        #print 'cols = {}'.format(c)

    def init_validators(self):
        self.a_s_row = [[0] * self.n for x in range(self.size[0])]
        self.a_s_col = [[0] * self.n for x in range(self.size[1])]
        self.a_s_dia_ne = [[0] * self.n for x in range(self.size[0] + self.size[1]-1)]
        self.a_s_dia_nw = [[0] * self.n for x in range(self.size[0] + self.size[1]-1)]
        self.s_row_rollup=0
        self.s_col_rollup=0
        self.s_dia_ne_rollup=0
        self.s_dia_nw_rollup=0

    def get_diagonal_coords(self,row, col):
        dc_nw = col - row + (len(self.r) - 1)
        dc_ne = row + col
        return (dc_nw, dc_ne)

    @staticmethod
    def get_rand(i):
        return reduce(lambda x,y: x&y, [random.getrandbits(64) for _ in range(i)])

    def validate(self):
        self.init_validators()
        for c in self.c:
            for r in self.r:
                #diagonal counter
                dc_nw,dc_ne = self.get_diagonal_coords(r,c)
                for i in self.l:
                    self.a_s_col[c][i] |= self.a_s_col[c][i - 1] & self.a_boards[r][c]
                    self.a_s_row[r][i] |= self.a_s_row[r][i - 1] & self.a_boards[r][c]
                    self.a_s_dia_nw[dc_nw][i] |= self.a_s_dia_nw[dc_nw][i - 1] & self.a_boards[r][c]
                    self.a_s_dia_ne[dc_ne][i] |= self.a_s_dia_ne[dc_ne][i - 1] & self.a_boards[r][c]
                self.a_s_col[c][0] |= self.a_boards[r][c]
                self.a_s_row[r][0] |= self.a_boards[r][c]
                self.a_s_dia_nw[dc_nw][0] |= self.a_boards[r][c]
                self.a_s_dia_ne[dc_ne][0] |= self.a_boards[r][c]

        # rollup columns. if result == 0 then ok
        for s in self.a_s_col:
            self.s_col_rollup |= s[-1]

        # rollup rows. if result == 0 then ok
        for s in self.a_s_row:
            self.s_row_rollup |= s[-1]

        # rollup nw diagonal. if result == 0 then ok
        for s in self.a_s_dia_nw:
            self.s_dia_nw_rollup|= s[-1]

        # rollup ne diagonal. if result == 0 then ok
        for s in self.a_s_dia_ne:
            self.s_dia_ne_rollup|= s[-1]

    def populate(self, times=1):
        for i in range(times):
            # pick random row and column
            row = random.randint(0,self.size[0]-1)
            col = random.randint(0,self.size[1]-1)

            # identify coresponding diagonals
            dc_nw,dc_ne = self.get_diagonal_coords(row,col)

            seed = self.get_rand(1)

            self.a_boards[row][col] |=  seed & \
                ( ~self.a_s_row[row][-2]) & \
                ( ~self.a_s_col[col][-2]) & \
                ( ~self.a_s_dia_ne[dc_ne][-2]) & \
                ( ~self.a_s_dia_nw[dc_nw][-2])

    def run(self):
        for i in range(1000/(self.n - 1)):
            self.populate(2)
            self.validate()

    def get_results(self):
        successes = self.find_successes()
        return self.get_queens(successes[-1][1])

    def find_successes(self,nof_boards=64):
        b = (self.s_col_rollup | self.s_row_rollup | \
             self.s_dia_nw_rollup | self.s_dia_ne_rollup)
        l=c=0
        res=[]
        while (l<nof_boards):
            if b & 1 == 0 :
                res.append((self.nof_queens(l),l))
            l += 1
            b >>= 1

        res.sort(key=lambda t:t[0])
        return res

    def nof_queens(self, bit):
        return len(self.get_queens(bit))

    def get_queens(self, bit):
        tot = 0
        coords=[]
        for r,row in enumerate(self.a_boards):
            for c,col in enumerate(row):
                if (col >> bit) & 1 :
                    coords.append((r,c))
        return coords


    @staticmethod
    def printBitMatrix(bit, matrix):
        def ft(r):
            o=''
            if type(r) is str:
                o = r
            else:
                o = 1 & (r >> bit )
            return '{:2}'.format(o)


        print('\n'.join([''.join(
            [ft(v) for v in rows]
            ) for rows in matrix]))

    def printBitStates(self,bit, what):
        if what == 'col':
            states = self.a_s_col
        else:
            states = self.a_s_row
        a_sr = [['val  : '] + ['{}'.format(x) for x in range(1,self.n+1)] ]+[
            ['{} {}:'.format(what,i+1)]+r for i,r in enumerate(states)]
        print '\n{} states'.format(what)
        self.printBitMatrix(bit,a_sr)

def bit_count(b,nof_bits=64):
    l=c=0
    while (l<nof_bits):
        c += (b & 1)
        l += 1
        b >>= 1
    return c

def bit_str(b):
    l=c=0
    s=''
    while (l<64):
        s = str(b & 1) + s
        l += 1
        b >>= 1
    return s

def print_histo(histo):
    for i,h in enumerate(histo):
        if h > 0:
            break;
    i -= 2
    if i < 0: i = 0
    print '\n'
    print '\n'.join([ ('{:<2} |{:>2} | {}').format(j,e, 'x'*e) for j,e in enumerate(histo) if j>=i ])
    print '\n'

if __name__ == '__main__':

    # 13 / 14 -> 0.227
    #q=QueensGame(1,4,4, [(0,0)])
    # 6 / 8 -> 0.400
    #q=QueensGame(2, 10, 4, [(9,0),(0,3)])
    # 0 / 1 -> 0.199
    #q=QueensGame(1, 6, 1, [(0,0)])
    # 2 / 3 -> 0.253
    #q=QueensGame(1,5,5, [(0,0),(2,3)])
    # 17 / 19 -> 1.570
    #q=QueensGame(1,20,20, [])
    # 51 / 58 -> 1.127
    #q=QueensGame(3,20,20, [(0,0),(0,1),(1,2),(4,2),(4,0),(15,19),(5,7)])
    #q=QueensGame(3,20,20, [])
    # 24 / 30 -> 0.514
    q=QueensGame(3,10, 15, [(0,0),(2,3),(1,2),(0,6),(6,0),(9,10)])

    QueensGame.printBitMatrix(0,q.a_boards)
    for i in range(1000/(q.n - 1)):
        q.populate(2)
        q.validate()

    '''
    for i in range(1):
        print_bit=i
        print '====================='
        print 'print bit: {}'.format(print_bit)
        QueensGame.printBitMatrix(print_bit,q.a_boards)
        q.printBitStates(print_bit,'row')
        q.printBitStates(print_bit,'col')

    print 'row  : {} {}'.format(bit_count(q.s_row_rollup), bit_str(q.s_row_rollup))
    print 'col  : {} {}'.format(bit_count(q.s_col_rollup), bit_str(q.s_col_rollup))
    res = bit_str(q.s_col_rollup | q.s_row_rollup)

    print 'tot  : {} {}'.format(res.count('1'), res)
    print 'fails: {}'.format(res.count("1"))
    '''

    successes = q.find_successes()
    histo=[0]
    c=2
    for n,i in successes:
        if len(histo) <= n:
            histo+=([0]*(n - len(histo)+1))

        histo[n]+=1

        c+=1
        if c < len(successes): continue

        print_bit=i
        print '====================='
        print 'print bit: {}'.format(print_bit)
        QueensGame.printBitMatrix(print_bit,q.a_boards)
        q.printBitStates(print_bit,'row')
        q.printBitStates(print_bit,'col')
        print 'queens found: {}'.format(q.nof_queens(i))

    print_histo(histo)
    print 'found successes: {} {}'.format(len(successes),successes)
