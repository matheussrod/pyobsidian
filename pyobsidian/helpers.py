"""
This module contains helper functions.
"""

import re

def convert_str_or_list_to_list(value: str | list[str]) -> list[str]:
    """Convert a string or a list of strings to a list of strings.
    
    Parameters
    ----------
    value : str | list[str]
        The value to be converted.
    
    Returns
    -------
    list[str]
        A list of strings.
    """
    if isinstance(value, str):
        return [value]
    else:
        return value

def has_yaml(content: str) -> bool:
    """Check if the given content has YAML.

    Parameters
    ----------
    content : str
        The content to be checked.

    Returns
    -------
    bool
        True if the content has YAML, False otherwise.
    """
    re_compile = re.compile(r'---(.*?)---', re.DOTALL)
    re_findall = re.findall(re_compile, content)
    if len(re_findall) == 0:
        return False
    return True

def read_file(path: str) -> str:
    """Read the content of a file.

    Parameters
    ----------
    path : str
        The path of the file to be read.

    Returns
    -------
    str
        The content of the file.
    """
    with open(path, 'r', encoding='utf8') as file:
         content = file.read()
    return content
