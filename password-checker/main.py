"""
The password checker is a small web service that calculates
a score for a given password.
"""
import math
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Password(BaseModel):
    """
    Helper model for data transfer.
    """
    password: str


@app.post("/check-password")
async def check_password(password: Password):
    """
    This is the main route of the service. It calculates
    all different checks and returns their result.
    :param password: Password to check as json body
    :type password: Password
    :return: List of password result maps
    :rtype: list(dict)
    """
    checks = [
        length_check,
        uppercase_check,
        lowercase_check,
        number_check,
        symbols_check,
        middle_numbers_or_symbols,
        letters_only,
        numbers_only,
        repeat_characters
    ]

    return [f(password.password) for f in checks]


def length_check(password: str):
    """
    Checks for the length of the password
    :param password: Password as string
    :type password: str
    :return: Result map specifying the length calculations
    :rtype: dict
    """
    length = len(password)
    return {
        "name": "Number of characters",
        "count": length,
        "bonus": length * 4,
        "type": "Addition"
    }


def uppercase_check(password: str):
    """
        Checks for the number of uppercase characters
        :param password: Password as string
        :type password: str
        :return: Result map specifying the uppercase calculations
        :rtype: dict
        """
    uppercase = sum(1 for c in password if c.isupper())
    return {
        "name": "Uppercase letters",
        "count": uppercase,
        "bonus": (len(password) - uppercase)*2,
        "type": "Addition"
    }


def lowercase_check(password: str):
    """
    Checks for the number of lowercase characters
    :param password: Password as string
    :type password: str
    :return: Result map specifying the lowercase calculations
    :rtype: dict
    """
    lowercase = sum(1 for c in password if c.islower())
    return {
        "name": "Lowercase letters",
        "count": lowercase,
        "bonus": (len(password) - lowercase)*2,
        "type": "Addition"
    }


def number_check(password: str):
    """
    Checks for the number of characters that are numeric
    :param password: Password as string
    :type password: str
    :return: Result map specifying the number calculations
    :rtype: dict
    """
    numbers = sum(1 for c in password if c.isnumeric())
    return {
        "name": "Numbers",
        "count": numbers,
        "bonus": numbers * 4,
        "type": "Addition"
    }


def symbols_check(password: str):
    """
    Checks for the number of symbol characters
    :param password: Password as string
    :type password: str
    :return: Result map specifying the symbol calculations
    :rtype: dict
    """
    symbols = sum(1 for c in password if not c.isalnum())
    return {
        "name": "Symbols",
        "count": symbols,
        "bonus": symbols * 6,
        "type": "Addition"
    }


def middle_numbers_or_symbols(password: str):
    """
    Checks for the number of characters that are in the
    middle of the string and are numeric or symbols
    :param password: Password as string
    :type password: str
    :return: Result map specifying the middle numbers/symbols calculations
    :rtype: dict
    """
    middle_symbols = sum(1 for c in password[1:-1] if not c.isalpha())
    return {
        "name": "Middle numbers or symbols",
        "count": middle_symbols,
        "bonus": middle_symbols * 6,
        "type": "Addition"
    }


def letters_only(password: str):
    """
    Checks if the password is letters only
    :param password: Password as string
    :type password: str
    :return: Result map specifying the letters only calculations
    :rtype: dict
    """
    only_letters = len(password) if password.isalnum() else 0
    return {
        "name": "Letters only",
        "count": only_letters,
        "bonus": -only_letters,
        "type": "Deduction"
    }


def numbers_only(password: str):
    """
    Checks if the password is numeric only
    :param password: Password as string
    :type password: str
    :return: Result map specifying the numbers only calculations
    :rtype: dict
    """
    only_numbers = len(password) if password.isnumeric() else 0
    return {
        "name": "Numbers only",
        "count": only_numbers,
        "bonus": -only_numbers,
        "type": "Deduction"
    }


def repeat_characters(password: str):
    """
    Checks for repeated characters in the password
    :param password: Password as string
    :type password: str
    :return: Result map specifying the repeated characters calculations
    :rtype: dict
    """
    num_rep_characters = 0
    score = 0
    for i in range(len(password)):
        repeated = False
        for j in range(len(password)):
            if i != j and password[i] == password[j]:
                repeated = True
                score += abs(len(password) / (j-i))
        if repeated:
            num_rep_characters += 1

    num_unique_chars = len(password) - num_rep_characters
    check_value = math.ceil(score / num_unique_chars) if num_unique_chars else math.ceil(score)

    return {
        "name": "Repeated Characters",
        "count": num_rep_characters,
        "bonus": -check_value,
        "type": "Deduction"
    }