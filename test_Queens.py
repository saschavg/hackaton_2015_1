from queens import *
import numpy as np
import unittest
import statistics as stat

class TestQueensGame(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_rand(self):
        def calc_rand(n):
            l=1000
            return [bit_count(QueensGame.get_rand(n))/64. for _ in range(l)]

        r = calc_rand(1)
        sd = np.std(r)
        m = np.mean(r)
        self.assertAlmostEqual(m,0.5,delta=0.06)
        self.assertAlmostEqual(sd,0.062,delta=0.005)

    def test_bit_count(self):
        self.assertEqual(64, bit_count(~0, 64))
        self.assertEqual(4, bit_count(~0, 4))
        self.assertEqual(2, bit_count(3))
        self.assertEqual(63, bit_count(sys.maxint))

    def test_boards_1x1(self):
        nof_boards=64
        q = QueensGame(1, 1, 1)
        #start with empty board
        self.assertEquals([[0]], q.a_boards)
        # each simulation has a 0.5 chance to get populated with a 1
        q.populate(1)
        # ensure some boards are populated
        self.assertNotEqual(0, bit_count(q.a_boards[0][0]))

        q.validate()
        successes = q.find_successes(nof_boards)
        self.assertEquals(len(successes) , nof_boards)
        # we expect that there at least one filled board
        # very little change that it is not: 0.5**64 = 5.4e-20
        self.assertEquals(successes[-1][0], 1)

    def test_validate(self):
        q = QueensGame(2, 2, 2)
        q.a_boards=[[1,1],[1,1]]
        q.validate()
        self.assertEqual([[1,1,0],[1,1,0]], q.a_s_col)
        self.assertEqual([[1,1,0],[1,1,0]], q.a_s_row)
        self.assertEqual(0, q.s_col_rollup)
        self.assertEqual(0, q.s_row_rollup)

        q = QueensGame(1, 2, 2)
        q.a_boards=[[1,1],[1,1]]
        q.validate()
        self.assertEqual([[1,1],[1,1]], q.a_s_col)
        self.assertEqual([[1,1],[1,1]], q.a_s_row)
        self.assertEqual(1, q.s_col_rollup)
        self.assertEqual(1, q.s_row_rollup)

        q = QueensGame(1, 2, 2)
        # board 0   board 1 other boards
        #   0 1       1 0     0 0
        #   1 1       0 0     0 0
        q.a_boards=[[2,1],[1,1]]

        # number of queens on board 0
        self.assertEqual(3, q.nof_queens(0))
        # number of queens on board 1
        self.assertEqual(1, q.nof_queens(1))
        # number of queens on board 2
        self.assertEqual(0, q.nof_queens(2))
        # number of queens on board 63
        self.assertEqual(0, q.nof_queens(63))
        q.validate()

        self.assertEqual([[3,0],[1,1]], q.a_s_col)
        self.assertEqual([[3,0],[1,1]], q.a_s_row)
        self.assertEqual(1, q.s_col_rollup)
        self.assertEqual(1, q.s_row_rollup)

        # board 0 is NOT ok and should not be returned
        self.assertEquals([],q.find_successes(1))
        # fetching the first 2 boards yields only board 1 as that is the only
        # one of the two with proper result
        self.assertEquals([(1,1)],q.find_successes(2))
        # fetching the first 3 boards yields only board 1 and 2 as they are the only
        # one of the fist three with proper result. They are sorted by numer of
        # queens on the board ( first param of the tuples)
        self.assertEquals([(0,2),(1,1)],q.find_successes(3))



    def test_boards_2x1(self):
        nof_boards=64
        res=[]
        # chance to populate a 2x1 board with 2 queens in one itteration
        # 0.5 * 0.5 * 0.5 = 0.125
        # we do a 1000 runs and avarage to calc the result
        for x in range(1000):
            q = QueensGame(2, 2, 1)
            for i in range(1):
                q.populate(2)
                q.validate()
            successes = q.find_successes(nof_boards)
            successes = [s[0] for s in successes ]
            res += successes
        self.assertAlmostEqual(0.125, res.count(2)*1./len(res), delta=0.05)
        self.assertEqual(nof_boards*1000, len(res))

    def test_boards_2x2(self):
        nof_boards=64
        res=[]
        for x in range(2000):
            q = QueensGame(2, 2, 2)
            for i in range(1):
                # change to fill the board with ones in 4 seeds
                # chance is 0.5^4 * 1.0 * 0.75 * 0.5 * 0.25 = 0.00586 ~ 1/170
                # chance to find an unfilled board ~ 169/170
                # chance that one out of 64 boards is filled ~ 1 - (169/170)^64
                q.populate(4)
                q.validate()
            successes = q.find_successes(nof_boards)
            successes = [s[0] for s in successes ]
            res += successes
        self.assertAlmostEqual(0.00586, res.count(4)*1./len(res), delta=0.0015)
        self.assertEqual(nof_boards*2000, len(res))

if __name__ == '__main__':
    unittest.main()
