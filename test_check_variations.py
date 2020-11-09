import unittest
from check_variations import check


class TestWinrates(unittest.TestCase):
    def test_check(self):
        self.assertFalse(check("../gogod_commentary/1960-69/1963-07-04b.sgf"))

if __name__ == '__main__':
    unittest.main()