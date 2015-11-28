from queens import *

import time

if __name__ == '__main__':
    start_time = time.time()

    # 2 / 3 -> 0.160
    #q=QueensGame(1,3,3, [(0,0)])
    # 6 / 8 -> 0.400
    #q=QueensGame(1, 10, 4, [(9,0),(0,3)])
    # 0 / 1 -> 0.199
    #q=QueensGame(0, 6, 1, [(0,0)])
    # 1 / 3 -> 0.253
    #q=QueensGame(0,5,5, [(0,0),(2,3)])
    # 17 / 19 -> 1.570
    #q=QueensGame(0,20,20, [])
    # 51 / 58 -> 1.127
    q=QueensGame(2,20,20, [(0,0),(0,1),(1,2),(4,2),(4,0),(15,19),(5,7)])
    #q=QueensGame(2,20,20, [])
    # 24 / 30 -> 0.514
    #q=QueensGame(2,10, 15, [(0,0),(2,3),(1,2),(0,6),(6,0),(9,10)])

    QueensGame.printBitMatrix(0,q.a_boards)
    while time.time() - start_time < 2:
        q.populate(100)

    #q.populate(1000)

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
        print 'queens found: {}'.format(q.nof_queens(i))

    print_histo(histo)
    print 'found successes: {} {}'.format(len(successes),successes)
