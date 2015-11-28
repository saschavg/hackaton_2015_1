from queens import *
import numpy as np
import unittest

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
        q = QueensGame(0, 1, 1)
        #start with empty board
        self.assertEquals([[0]], q.a_boards)
        # each simulation has a 0.5 chance to get populated with a 1
        q.populate(1)
        # ensure some boards are populated
        self.assertNotEqual(0, bit_count(q.a_boards[0][0]))

        successes = q.find_successes(nof_boards)
        self.assertEquals(len(successes) , nof_boards)
        # we expect that there at least one filled board
        # very little change that it is not: 0.5**64 = 5.4e-20
        self.assertEquals(successes[-1][0], 1)

    def test_init(self):
        q = QueensGame(0, 2, 2, queens=[[0,0]])
        self.assertEqual(q.n,1)
        self.assertEqual(range(2),q.r)
        self.assertEqual(range(2),q.c)
        self.assertEqual([[~0,0],[0,0]], q.a_boards)

    def test_update_queen_count(self):
        q = QueensGame(0, 2, 2, queens=[[0,0]])
        s = [0]*q.n

        q.update_queen_count(s,1,0)
        self.assertEqual(0, s[-1])

        q.update_queen_count(s,0,0)
        self.assertEqual(~0, s[-1])

        q.update_queen_count(s,1,0)
        self.assertEqual(~0, s[-1])

        q = QueensGame(1, 2, 2, queens=[[0,0]])
        s = [0]*q.n

        q.update_queen_count(s,1,0)
        self.assertEqual([0,0], s)

        q.update_queen_count(s,0,0)
        self.assertEqual([~0,0], s)

        q.a_boards[1][1]= ~0
        q.update_queen_count(s,1,1)
        self.assertEqual([~0,~0], s)

        q.a_boards[1][0]= ~0
        q.update_queen_count(s,1,0)
        self.assertEqual([~0,~0], s)


    def test_position_needs_lock(self):
        true=~0
        false=0
        q = QueensGame(0, 2, 2, queens=[[0,0]])
        self.assertEqual(true, q.position_needs_lock(1,1))
        self.assertEqual(true, q.position_needs_lock(1,0))
        self.assertEqual(true, q.position_needs_lock(0,0))
        self.assertEqual(true, q.position_needs_lock(0,1))

        q = QueensGame(1, 2, 2, queens=[[0,0]])
        self.assertEqual(false, q.position_needs_lock(1,1))
        self.assertEqual(false, q.position_needs_lock(1,0))
        self.assertEqual(false, q.position_needs_lock(0,0))
        self.assertEqual(false, q.position_needs_lock(0,1))

        q = QueensGame(0, 2, 3, queens=[[0,0]])
        self.assertEqual(false, q.position_needs_lock(1,2))
        self.assertEqual(true, q.position_needs_lock(0,2))
        self.assertEqual(true, q.position_needs_lock(1,0))
        self.assertEqual(true, q.position_needs_lock(0,0))
        self.assertEqual(true, q.position_needs_lock(0,1))

        q = QueensGame(0, 3, 2, queens=[[0,0]])
        self.assertEqual(false, q.position_needs_lock(2,1))
        self.assertEqual(true, q.position_needs_lock(2,0))
        self.assertEqual(true, q.position_needs_lock(1,0))
        self.assertEqual(true, q.position_needs_lock(0,0))
        self.assertEqual(true, q.position_needs_lock(0,1))

    def test_position_needs_lock_1(self):
        true=~0
        false=0
        q = QueensGame(1, 3, 3, queens=[(0,0),(1,0)])
        #q.printBitMatrix(0,q.a_boards)
        #q.printBitMatrix(0,q.a_boards_locked)
        self.assertEqual(true, q.position_needs_lock(0,0))
        self.assertEqual(true, q.position_needs_lock(0,1))
        self.assertEqual(false, q.position_needs_lock(0,2))

        self.assertEqual(true, q.position_needs_lock(1,0))
        self.assertEqual(true, q.position_needs_lock(1,1))
        self.assertEqual(false, q.position_needs_lock(1,2))

        self.assertEqual(true, q.position_needs_lock(2,0))
        self.assertEqual(false, q.position_needs_lock(2,1))
        self.assertEqual(false, q.position_needs_lock(2,2))

    def test_update_locked_positions(self):
        q = QueensGame(0, 2, 2)
        self.assertEqual([[0,0],[0,0]],q.a_boards_locked)
        q.a_boards[0][0] = ~0
        q.update_locked_positions(0,0)
        self.assertEqual([[~0,~0],[~0,~0]],q.a_boards_locked)

        q = QueensGame(0, 3, 2)
        self.assertEqual([[0,0],[0,0],[0,0]],q.a_boards_locked)
        q.a_boards[0][0] = ~0
        q.update_locked_positions(0,0)
        self.assertEqual([[~0,~0],[~0,~0],[~0,0]],q.a_boards_locked)

    def test_lock_position(self):
        q = QueensGame(0, 2, 2, queens=[[0,0]])
        self.assertEqual([[~0,~0],[~0,~0]],q.a_boards_locked)
        q.lock_position(~0,1,1)
        self.assertEqual([[~0,~0],[~0,~0]],q.a_boards_locked)

        q = QueensGame(0, 2, 2, queens=[[0,0],[0,1]])
        self.assertEqual([[~0,~0],[~0,~0]],q.a_boards_locked)
        q.lock_position(~0,1,1)
        self.assertEqual([[~0,~0],[~0,~0]],q.a_boards_locked)

    def test_boards_2x1(self):
        nof_boards=64
        res=[]
        # chance to populate a 2x1 board with 2 queens in one itteration
        # 0.5 * 0.5 * 0.5 = 0.125
        # we do a 1000 runs and avarage to calc the result
        for x in range(1000):
            q = QueensGame(1, 2, 1)
            q.populate(2)
            successes = q.find_successes()
            successes = [s[0] for s in successes ]
            res += successes
        #print 'xx: {} of {}\n{}'.format(res.count(2), len(res), res)
        self.assertAlmostEqual(0.125, res.count(2)*1./len(res), delta=0.05)
        self.assertEqual(nof_boards*1000, len(res))

    def test_boards_2x2(self):
        nof_boards=64

        q = QueensGame(0, 2, 2,[(0,0)])
        # change to fill the board with additional queens == 0 if we can only
        # see 0 queens
        q.populate(100)
        successes = q.find_successes(nof_boards)
        successes = [s[0] for s in successes ]
        self.assertEqual(0, successes.count(4))
        self.assertEqual(nof_boards, len(successes))

        q = QueensGame(0, 3, 3,[(0,0)])
        # change to fill the board with additional queens == 0 if we can only
        # see 0 queens
        q.populate(100)
        successes = q.find_successes(nof_boards)
        successes = [s[0] for s in successes ]
        self.assertEqual(0, successes.count(3))
        self.assertGreater(successes.count(2),1)
        self.assertEqual(nof_boards, len(successes))

        q = QueensGame(1, 3, 3,[(0,0)])
        # change to fill the board with additional queens
        q.populate(100)
        successes = q.find_successes(nof_boards)
        successes = [s[0] for s in successes ]
        self.assertEqual(0,successes.count(4))
        self.assertEqual(nof_boards, len(successes))

        res=[]
        for x in range(100):
            q = QueensGame(2, 2, 2)
            # change to fill the board with ones in 4 seeds == 0 if we can only
            # see 2 queens
            q.populate(4)
            successes = q.find_successes(nof_boards)
            successes = [s[0] for s in successes ]
            res += successes
        self.assertEqual(0, res.count(4))
        self.assertEqual(nof_boards*100, len(res))

        res=[]
        for x in range(2000):
            q = QueensGame(3, 2, 2)
            # change to fill the board with ones in 4 seeds
            # chance is 0.5^4 * 1.0 * 0.75 * 0.5 * 0.25 = 0.00586 ~ 1/170
            # chance to find an unfilled board ~ 169/170
            # chance that one out of 64 boards is filled ~ 1 - (169/170)^64
            q.populate(4)
            successes = q.find_successes(nof_boards)
            successes = [s[0] for s in successes ]
            res += successes
        self.assertAlmostEqual(0.00586, res.count(4)*1./len(res), delta=0.0015)
        self.assertEqual(nof_boards*2000, len(res))

if __name__ == '__main__':
    unittest.main()
