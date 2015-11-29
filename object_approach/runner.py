from queens_sim import *
import time

if __name__ == '__main__':
    end_time = time.time() + 1.8

    b = Board(4,8)
    Queen( b.position(3,1) )
    Queen( b.position(2,6) )

    game = QueensGame(b,2)

    print game.board
    #queens = game.run(endtime=end_time)
    queens = game.run(runs=100)
    print 'found max queens: {} {}'.format(len(queens),queens)
    print game.board

