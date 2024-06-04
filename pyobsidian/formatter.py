"""
This module contains the classes that represent formatters.

Formatters are used to format the content that will be added in notes.
"""

from abc import ABC, abstractmethod
from typing import Self
from pyobsidian.helpers import convert_str_or_list_to_list

class Formatter(ABC):
    """Base class for all formatters."""
    @abstractmethod
    def __repr__(self: Self) -> str:
        ...

    @abstractmethod
    def format(self: Self, value: str | list[str]) -> str | list[str]:
        """Format the content.

        Parameters
        ----------
        value : str | list[str]
            The content to format.

        Returns
        -------
        str | list[str]
            The formatted content.
        """
        ...

class FormatterYaml(Formatter):
    """This formatter just converts the content to list."""
    def __repr__(self: Self) -> str:
        return 'FormatterYaml()'
    
    def format(self: Self, value: str | list[str]) -> list[str]:
        value_md = convert_str_or_list_to_list(value)
        return value_md
    
class FormatterTagYaml(FormatterYaml):
    def __repr__(self: Self) -> str:
        return 'FormatterTagYaml()'

class FormatterTagInline(Formatter):
    """This formatter adds "#" to each word entered and adds two line breaks at the beginning and end."""
    def __repr__(self: Self) -> str:
        return 'FormatterTagInline()'
    
    def format(self: Self, value: str | list[str]) -> str:
        value = convert_str_or_list_to_list(value)
        value_format = [
            tag if tag.startswith('#') else f'#{tag}'
            for tag in value
        ]
        value_md = '\n\n' + ' '.join(value_format) + '\n\n'
        return value_md

class FormatterTagOpMkHeader(FormatterTagInline):
    """This formatter adds "#" to each word entered and adds two line breaks at the beginning and end."""
    def __repr__(self: Self) -> str:
        return 'FormatterTagOpMkHeader()'

class FormatterRelatedNoteYaml(Formatter):
    """This formatter adds "[[" and "]]" to each word entered and convert to list."""
    def __repr__(self: Self) -> str:
        return 'FormatterRelatedNoteYaml()'
    
    def format(self: Self, value: str | list[str]) -> list[str]:
        value = convert_str_or_list_to_list(value)
        value_md = [
            v if v.startswith('[[') else f'[[{v}]]'
            for v in value
        ]
        return value_md
    
class FormatterRelatedNoteInline(Formatter):
    """This formatter adds "[[" and "]]" to each word entered and adds two line breaks at the beginning and end."""
    def __repr__(self: Self) -> str:
        return 'FormatterRelatedNoteInline()'
    
    def format(self: Self, value: str | list[str]) -> str:
        value = convert_str_or_list_to_list(value)
        value_format = [
            note if note.startswith('[[') else f'[[{note}]]'
            for note in value
        ]
        value_md = '\n\n- ' + '\n- '.join(value_format) + '\n\n'
        return value_md

class FormatterRelatedNoteOpMkHeader(FormatterRelatedNoteInline):
    """This formatter adds "[[" and "]]" to each word entered and adds two line breaks at the beginning and end."""
    def __repr__(self: Self) -> str:
        return 'FormatterRelatedNoteOpMkHeader()'

class FormatterContentYaml(FormatterYaml):
    def __repr__(self: Self) -> str:
        return 'FormatterContentYaml()'

class FormatterContentInline(Formatter):
    """This formatter adds two line breaks at the beginning and end."""
    def __repr__(self: Self) -> str:
        return 'FormatterContentInline()'
    
    def format(self: Self, value: str | list[str]) -> str:
        value = convert_str_or_list_to_list(value)
        return '\n\n' + '\n\n'.join(value) + '\n\n'

class FormatterContentOpMkHeader(FormatterContentInline):
    ...
