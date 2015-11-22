#!/usr/bin/env python
import random
import sys
import numpy
import ctypes


class QueensGame():

    def __init__(self, n, r, c):
        self.n = n+1
        self.l = range(1, self.n)
        self.l.reverse()
        self.size = (r, c)
        self.c = range(c)
        self.r = range(r)
        self.init_validators()
        #self.a_boards = [ [ self.get_rand(3) for _ in xrange(c)] for y in xrange(r)]
        self.a_boards = [ [ 0 for _ in xrange(c)] for y in xrange(r)]
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

    @staticmethod
    def get_rand(i):
        return reduce(lambda x,y: x&y, [random.getrandbits(64) for _ in range(i)])

    def validate(self):
        self.init_validators()
        for x in self.c:
            for y in self.r:
                #diagonal counter
                dc_nw = x - y + (len(self.r) - 1)
                dc_ne = y + x
                #dc_ne = x +y -len(self.r)-1 + y
                for i in self.l:
                    self.a_s_col[x][i] |= self.a_s_col[x][i - 1] & self.a_boards[y][x]
                    self.a_s_row[y][i] |= self.a_s_row[y][i - 1] & self.a_boards[y][x]
                    self.a_s_dia_nw[dc_nw][i] |= self.a_s_dia_nw[dc_nw][i - 1] & self.a_boards[y][x]
                    self.a_s_dia_ne[dc_ne][i] |= self.a_s_dia_ne[dc_ne][i - 1] & self.a_boards[y][x]
                self.a_s_col[x][0] |= self.a_boards[y][x]
                self.a_s_row[y][0] |= self.a_boards[y][x]
                self.a_s_dia_nw[dc_nw][0] |= self.a_boards[y][x]
                self.a_s_dia_ne[dc_ne][0] |= self.a_boards[y][x]

        '''
        for y in self.r:
            for x in self.c:
                for i in self.l:
                    self.a_s_row[y][i] |= self.a_s_row[y][i - 1] & self.a_boards[y][x]
                self.a_s_row[y][0] |= self.a_boards[y][x]

        for x in self.c:
            for y in reversed(self.r):
                dc = x-y+len(self.r)-1
                print dc
                for i in self.l:
                    self.a_s_dia_nw[dc][i] |= self.a_s_dia_nw[dc][i - 1] & self.a_boards[y][x]
                self.a_s_dia_nw[y][0] |= self.a_boards[y][x]
        '''


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
            row = random.randint(0,self.size[0]-1)
            col = random.randint(0,self.size[1]-1)

            dc_nw = col - row + (len(self.r) - 1)
            dc_ne = row + col

            seed = self.get_rand(1)
            #seed = ~0

            self.a_boards[row][col] |=  seed & \
                ( ~self.a_s_row[row][-2]) & \
                ( ~self.a_s_col[col][-2]) & \
                ( ~self.a_s_dia_ne[dc_ne][-2]) & \
                ( ~self.a_s_dia_nw[dc_nw][-2])



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
        tot = 0
        for row in self.a_boards:
            for col in row:
                tot += (col >> bit) & 1
        return tot


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

    q = QueensGame(1,4,4)
    for i in range(100):
        q.populate(2)
        q.validate()
        #QueensGame.printBitMatrix(0,q.a_boards)
        #print


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

    successes = q.find_successes()
    histo=[0]*30
    for n,i in successes:
        histo[n]+=1

        print_bit=i
        print '====================='
        print 'print bit: {}'.format(print_bit)
        QueensGame.printBitMatrix(print_bit,q.a_boards)
        q.printBitStates(print_bit,'row')
        q.printBitStates(print_bit,'col')
        print 'queens found: {}'.format(q.nof_queens(i))
    print_histo(histo)
    print 'found successes: {} {}'.format(len(successes),successes)
