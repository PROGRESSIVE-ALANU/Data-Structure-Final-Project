"""Unit tests for functions.py. Run with:  python -m unittest unit_test -v"""

import unittest

from functions import (
    add,
    is_even,
    factorial,
    is_palindrome,
    celsius_to_fahrenheit,
    fizzbuzz,
)


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add(-4, -6), -10)

    def test_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestIsEven(unittest.TestCase):
    def test_even(self):
        self.assertTrue(is_even(4))

    def test_odd(self):
        self.assertFalse(is_even(7))

    def test_zero(self):
        self.assertTrue(is_even(0))

    def test_negative(self):
        self.assertTrue(is_even(-2))


class TestFactorial(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_small_number(self):
        self.assertEqual(factorial(5), 120)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            factorial(2.5)


class TestIsPalindrome(unittest.TestCase):
    def test_simple_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_phrase_with_spaces_and_caps(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_empty_string(self):
        self.assertTrue(is_palindrome(""))


class TestCelsiusToFahrenheit(unittest.TestCase):
    def test_freezing(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)

    def test_boiling(self):
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_minus_forty(self):
        self.assertEqual(celsius_to_fahrenheit(-40), -40)


class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        self.assertEqual(fizzbuzz(9), "Fizz")

    def test_buzz(self):
        self.assertEqual(fizzbuzz(10), "Buzz")

    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(30), "FizzBuzz")

    def test_plain_number(self):
        self.assertEqual(fizzbuzz(7), "7")


if __name__ == "__main__":
    unittest.main()
