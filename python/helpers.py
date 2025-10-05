import re


def is_match(text, pattern) -> bool:
    """
    Check if a given string matches a given regex pattern.

    Args:
        text (str): The string to be checked.
        pattern (str): The regex pattern to be matched.

    Returns:
        bool: True if the string matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, text))


def remove_undesired_chars(text: str):
    """
    Remove undesired characters from a given string.

    Args:
        text (str): The string from which to remove undesired characters.

    Returns:
        str: The string with undesired characters removed.

    Undesired characters are defined as any of the following: space, newline, tab, or carriage return.
    """
    undeesired = [" ", "\n", "\t", "\r"]

    for char in undeesired:
        text = text.replace(char, "")

    return text


def remove_newlines(text: str):
    """
    Remove newlines from a given string.

    Args:
        text (str): The string from which to remove newlines.

    Returns:
        str: The string with newlines removed.
    """
    return text.replace("\n", "")


def remove_prefix(text: str, prefix: str):
    """
    Remove a prefix from a given string.

    Args:
        text (str): The string from which to remove the prefix.
        prefix (str): The prefix to be removed.

    Returns:
        str: The string with the prefix removed.
    """
    return text.replace(prefix, "", 1)


def remove_suffix(text: str, suffix: str):
    """
    Remove a suffix from a given string.

    Args:
        text (str): The string from which to remove the suffix.
        suffix (str): The suffix to be removed.

    Returns:
        str: The string with the suffix removed.
    """
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def remove_begin_end(text: str, string: str):
    """
    Remove a given string from both the beginning and end of a given string.

    Args:
        text (str): The string from which to remove the given string.
        string (str): The string to be removed from the beginning and end.

    Returns:
        str: The string with the given string removed from the beginning and end.
    """
    text = remove_prefix(text, string)
    text = remove_suffix(text, string)

    return text


def parsing_error(error: str, line: int) -> str:
    """
    Return a string representing a parsing error.

    Args:
        error (str): The error message.
        line (int): The line number where the error occurred.

    Returns:
        str: A string representing the parsing error.
    """
    return f"Error: {error} (line {line})"


def is_encapsuled_with(char: str, text: str) -> bool:
    """
    Check if a given string is begning and ending with a given character.

    Args:
        char (str): The character to check for encapsulation.
        text (str): The string to be checked.

    Returns:
        bool: True if the string is encapsulated with the character, False otherwise.
    """
    return text.startswith(char) and text.endswith(char)
