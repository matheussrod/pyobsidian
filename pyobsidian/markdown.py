"""
This module contains the classes that manipulate markdown content.
"""

import re
from typing import Self

MkHeader = list[dict[str, int | str]]
MkLevel = dict[str, MkHeader]
Operator = dict[str, str | int]

def parse_markdown(markdown: str) -> str:
    """Parse the markdown string.

    Parameters
    ----------
    markdown : str
        The markdown string to parse.

    Returns
    -------
    str
        The parsed markdown string.
    """
    return '\\n'.join(markdown.split('\\n'))

class MkHeaderLevels:
    """Get the levels of the headers in a markdown.

    Parameters
    ----------
    markdown : str
        The markdown string to parse.

    Returns
    -------
    MkLevel
        The levels of the headers in the markdown.
    """
    __pattern = r'(#{1,6})\s(.*)'
    def __init__(self: Self, markdown: str) -> None:
        self.__markdown = markdown

    @property
    def markdown(self: Self) -> str:
        """Markdown parsed.
        
        Returns
        -------
        str
            The markdown parsed.
        """
        return parse_markdown(self.__markdown)

    @property
    def pattern(self: Self) -> str:
        """The pattern to match the headers.

        Returns
        -------
        str
            The pattern to match the headers.
        """
        return self.__pattern

    @staticmethod
    def get_headers(markdown: str, pattern: re.Pattern[str]) -> MkHeader:
        """Get the headers in the markdown string.

        Parameters
        ----------
        markdown : str
            The markdown string to parse.
        pattern : re.Pattern[str]
            The pattern to match the headers.

        Returns
        -------
        MkHeader
            The headers in the markdown string.
        """
        headers = [
            {
                'start': m.start(), 
                'end': m.end(),
                'level': len(m.group(1)),
                'content': m.group(2)
            }
            for m in re.finditer(pattern, markdown)
        ]
        return headers

    def get_levels(self: Self) -> MkLevel:
        """Get the levels of the headers in the markdown string.

        Returns
        -------
        MkLevel
            The levels of the headers in the markdown string.
        """
        result: MkLevel = {}
        c_pattern = re.compile(self.pattern, re.MULTILINE)
        headers = self.get_headers(self.markdown, c_pattern)        
        for header in headers:
            level = str(header['level'])
            if level not in result:
                result[level] = []
            result[level].append({
                'start': header['start'],
                'end': header['end'],
                'content': header['content']
            })
        return result
