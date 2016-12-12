import unittest
from lebonprix.lr import LinearRegression
import numpy as np
import numpy.testing as npt


class TestLinearRegression(unittest.TestCase):
    def setUp(self):
        self.subject = LinearRegression()

    def test_linear_regression(self):
        x = np.array([[2012, 24000, 1, 0],
		              [2013, 50000, 0, 0],
		              [2012, 38000, 0, 0],
		              [2012, 31000, 1, 1]])
        y = np.array([21000,
                      21900,
                      22000,
                      22440])
        guess = np.array([[2012, 24000, 1, 0]])
        print(self.subject.lr(x, y, x))


if __name__  == '__main__':
    unittest.main()
