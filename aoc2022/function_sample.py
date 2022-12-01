from typing import List


def add_two_positive_numbers(x: int, y: int) -> int:
    """Add two positive numbers."""
    # Purposely silly if statement to show off regex in test.
    if x <= 0:
        raise ValueError("x must be positive.")
    if y <= 0:
        raise ValueError("y must be positive.")
    return x + y


# ----


def square_int_and_add_one(x: int) -> int:
    """
    Square an int and add one.

    Note:
    ----
    This function is purposely convoluted for testing purposes.

    """
    return add_one(square_int(x))


def square_int(x: int) -> int:
    """Square integer."""
    return x**2


def add_one(x: int) -> int:
    """Add one to integer."""
    return x + 1


# -----


def strip_numbers_bad_function(s: str) -> str:
    """
    Remove numbers from a string.

    Note:
    ----
        This function purposely does not work, to show off testing.
        It will return strings containing the number 9.

    """
    # Remove the `letter == 9` to see the test fail.
    return "".join(letter for letter in s if letter.isalpha() or letter == 9)


def sum_up_integers(nums: List[int]) -> int:
    """Sum up integers."""
    return sum(nums)


def expensive_function():
    """Fake an expensive function with this."""
    print("Hello! I'm expensive!")


def call_expensive_function() -> bool:
    """Emulate a call to an expensive function."""
    expensive_function()
    return True
