import unittest
from lebonprix.lr import LinearRegression
import numpy as np
import numpy.testing as npt


class TestLinearRegression(unittest.TestCase):
    def setUp(self):
        self.subject = LinearRegression()
        self.x = np.array([[2012, 24000, 1, 0],
		                   [2013, 50000, 0, 0],
		                   [2012, 38000, 0, 0],
		                   [2012, 31000, 1, 1]])
        self.y = np.array([21000,
                           21900,
                           22000,
                           22440])

    def test_linear_regression_returns_correct_guess(self):
        guess = np.array([[2012, 24000, 1, 0]])
        res = self.subject.lr(self.x, self.y, guess)
        npt.assert_array_equal(res, [21000])

    def test_linear_regression_returns_array_of_results(self):
        res = self.subject.lr(self.x, self.y, self.x)
        npt.assert_array_equal(res, [21000, 21900, 22000, 22440])