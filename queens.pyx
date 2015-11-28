#!/usr/bin/env python
import random
import sys
import ctypes
import time

class QueensGame():

    def __init__(self, n, r, c, queens=[]):
        self.start_queens = queens
        self.n = n+1
        self.c = range(c)
        self.r = range(r)
        self.l = r
        self.a_boards = [ [ 0 for _ in xrange(c)] for y in xrange(r)]
        self.a_boards_locked = [ [ 0 for _ in xrange(c)] for y in xrange(r)]

        for q in self.start_queens:
            self.a_boards[q[0]][q[1]] = ~0
            self.update_locked_positions(q[0],q[1])


    @staticmethod
    def get_rand(i):
        return reduce(lambda x,y: x&y, [random.getrandbits(64) for _ in range(i)])

    def update_queen_count_2(self,s,l,el):
        i=l
        while i>0 :
            s[i] |= (s[i - 1] & el)
            i -= 1
        s[0] |= el

    def update_queen_count(self,s,row,col):
        i=len(s)-1
        while i>0 :
            s[i] |= (s[i - 1] & self.a_boards[row][col])
            i-=1
        s[0] |= self.a_boards[row][col]

    def populate(self, times=1):
        for i in range(times):
            # pick random row and col
            row = random.randint(0,len(self.r)-1)
            col = random.randint(0,len(self.c)-1)

            seed = self.get_rand(1)

            #place queen if position not locked
            self.a_boards[row][col] |= (seed & ~self.a_boards_locked[row][col])
            self.update_locked_positions(row,col)

    def update_locked_positions(self,row,col):
        # for every position in sight of the given coordinate, check if the max
        # number of queens in sight for that position is reached. if so then we
        # lock that position.

        # check the positions in the column
        for r in self.r:
            self.lock_position( self.position_needs_lock(r,col) ,r,col)


        # check the positions in the row and diagonals
        for c in self.c:
            self.lock_position( self.position_needs_lock(row,c) ,row,c)

            dr = row - (c-col)
            if dr >= 0 and dr < len(self.r):
                self.lock_position( self.position_needs_lock(dr,c) ,dr,c)

            dr = row + (c-col)
            if dr >= 0 and dr < len(self.r):
                self.lock_position( self.position_needs_lock(dr,c) ,dr,c)

    def position_needs_lock(self,row,col):
        # if the position is already locked or it contains already a queen we
        # keep it locked
        s = [0] * self.n
        s[0] = self.a_boards[row][col]
        l= len(s)-1

        # count queens in sight within current column
        for r in self.r:
            if r == row: continue
            self.update_queen_count_2(s,l,self.a_boards[r][col])

        for c in self.c:
            if c == col: continue

            # count queens in sight within current row
            self.update_queen_count_2(s,l,self.a_boards[row][c])

            # count queens in sight within current diagonals
            dr = row - (c-col)
            if dr >= 0 and dr < self.l:
                self.update_queen_count_2(s,l,self.a_boards[dr][c])

            dr = row + (c-col)
            if dr >= 0 and dr < self.l:
                self.update_queen_count_2(s,l,self.a_boards[dr][c])
        return s[-1]

    def lock_position(self,need_lock, row, col):
        # lock column
        has_queen = self.a_boards[row][col]
        self.a_boards_locked[row][col] |= need_lock

        # if position already contains a queen and it needs a lock, then we need
        # to lock all the possible locations in sight of the current position
        for r in self.r:
            self.a_boards_locked[r][col] |= need_lock & has_queen

        for c in self.c:
            # lock row
            self.a_boards_locked[row][c] |= need_lock & has_queen

            # lock diagonals
            dr = row - (c-col)
            if dr >= 0 and dr < self.l:
                self.a_boards_locked[dr][c] |= need_lock & has_queen

            dr = row + (c-col)
            if dr >= 0 and dr < self.l:
                self.a_boards_locked[dr][c] |= need_lock & has_queen

    def find_successes(self,nof_boards=64):
        l=0
        res=[]
        while (l<nof_boards):
            res.append((self.nof_queens(l),l))
            l += 1

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

