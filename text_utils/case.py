import re

def to_snake_case(text: str) -> str:
    """
    Convert a camelCase string to snake_case.

    Args:
        text (str): The input string to convert.

    Returns:
        str: The snake_case version of the input.

    Raises:
        TypeError: If input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")

    if not text:
        return ""

    # Split on uppercase letters, preserving consecutive uppercase letters as a word
    # e.g., XMLHttpRequest → xml_http_request
    result = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
    # Handle consecutive uppercase letters (e.g., XML) by not splitting them
    result = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', result)
    return result.lower()

def to_camel_case(text: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Args:
        text (str): The input string to convert.

    Returns:
        str: The camelCase version of the input.

    Raises:
        TypeError: If input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")

    if not text:
        return ""

    # Split on underscores and capitalize the first letter of each word after the first
    words = text.split('_')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])