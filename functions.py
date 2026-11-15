"""A few simple Python functions to practice unit testing."""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def is_even(n):
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


def factorial(n):
    """Return n! for a non-negative integer n."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_palindrome(text):
    """Return True if text reads the same forwards and backwards
    (ignoring case, spaces and punctuation)."""
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def celsius_to_fahrenheit(celsius):
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def fizzbuzz(n):
    """Return 'Fizz' for multiples of 3, 'Buzz' for multiples of 5,
    'FizzBuzz' for multiples of both, otherwise the number as a string."""
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
