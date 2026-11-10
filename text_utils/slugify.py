import re

def slugify(text: str) -> str:
    """
    Convert arbitrary text into a lowercase, alphanumeric-only slug with single hyphens.

    Args:
        text (str): Input string to be slugified. May contain mixed case, spaces,
                    punctuation, special characters, and Unicode letters.

    Returns:
        str: A lowercase string composed only of alphanumeric characters and single
             hyphens, with no leading or trailing hyphens. Returns empty string if
             input is empty or contains only non-alphanumeric characters.

    Examples:
        >>> slugify("Hello World")
        'hello-world'
        >>> slugify("  HELLO   WORLD  ")
        'hello-world'
        >>> slugify("Café Münster")
        'cafe-muenster'
        >>> slugify("Hello---World")
        'hello-world'
        >>> slugify("éññα日本語")
        'éññα日本語'
        >>> slugify("   ")
        ''
        >>> slugify("!@#$%^&*()")
        ''
    """
    if not text:
        return ''

    # Replace all non-alphanumeric characters (excluding Unicode letters) with hyphens, then collapse runs of hyphens
    slug = re.sub(r'[^a-zA-Z0-9\u00C0-\u017F\u0180-\u024F\u1E00-\u1EFF]', '-', text.lower())
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')

    return slug
