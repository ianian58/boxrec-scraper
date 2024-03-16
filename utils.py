def safe_int_convert(value):
    """
    Safely converts a value to an integer.

    Args:
        value: The value to convert.

    Returns:
        The integer value, or None if conversion fails.
    """
    try:
        return int(value)
    except ValueError:
        return None

def extract_attribute(cell, tag, class_name, split_char=None, index=None, first_char=False):
    """
    Extracts an attribute from a BeautifulSoup cell.

    Args:
        cell: The BeautifulSoup object to search within.
        tag: The HTML tag to search for.
        class_name: The class name to search for.
        split_char: Character to split the result on, if any.
        index: Index of the split result to return, if split_char is used.
        first_char: Whether to return only the first character of the result.

    Returns:
        The extracted attribute, or None if not found.
    """
    element = cell.find(tag, class_=class_name)
    if not element:
        return None
    result = element.get('class')[1] if class_name else element['src']
    if split_char:
        result = result.split(split_char)[index]
    return result[0].upper() if first_char else result.upper()