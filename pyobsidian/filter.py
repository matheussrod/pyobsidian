"""
This module contains the classes that represent Obsidian filters.
Filters are used to search through Obsidian notes. 
See [searchby](searchby.md) to understand how filters are used.

A filter is composed of one or more fields, each field having an associated mode.
Each field has a key, value, and occurrence.

- key: The key of the field. Defines which search method will be used. See [get_search_strategies](searchby.md) for more information.
- value: The value of the field. Values that will be searched based on the chosen search method
- occurrence: The occurrence of the field value. Can be 'inline', 'yaml', or 'file'.
    - inline: occurs inline
    - yaml: occurs in yaml
    - file: both inline and yaml
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self, Iterator

FilterMode = Literal['and', 'or']
FieldKey = str
FieldValue = str | list[str]
FieldOcurrence = Literal['inline', 'yaml', 'file']

class Field:
    """Represents a filter field.

    Parameters
    ----------
    key : FieldKey
        The key of the field
    value : FieldValue
        The value of the field
    occurrence : FieldOcurrence
        The occurrence of the field
    """
    def __init__(
        self: Self, 
        key: FieldKey, 
        value: FieldValue, 
        occurrence: FieldOcurrence
    ) -> None:
        self.__key = key
        self.__value = value
        self.__occurrence = occurrence

    @property
    def key(self: Self) -> FieldKey:
        """The key of the field"""
        return self.__key
    
    @property
    def value(self: Self) -> FieldValue:
        """The value of the field"""
        return self.__value
    
    @property
    def occurrence(self: Self) -> FieldOcurrence:
        """The occurrence of the field"""
        return self.__occurrence
    
    def __repr__(self) -> str:
        return f"Field('{self.key}', '{self.value}', '{self.occurrence}')"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Field):
            return False
        return self.key == value.key \
           and self.value == value.value \
           and self.occurrence == value.occurrence

@dataclass
class FilterField:
    """Represents a filter field.

    Parameters
    ----------
    field : Field
        The filter field
    mode : FilterMode
        The mode of the filter
    """
    field: Field
    mode: FilterMode

class Filter:
    """Represents a filter for notes.

    Parameters
    ----------
    fields : list[FilterField]
        The list of filter fields
    """
    def __init__(self: Self, fields: list[FilterField] = []):
        self.__fields = fields

    def __repr__(self: Self) -> str:
        return f"Filter({self.fields})"
    
    def __iter__(self: Self) -> Iterator[FilterField]:
        for field in self.fields:
            yield field

    def __len__(self: Self):
        return len(self.fields)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Filter):
            return False
        return self.fields == value.fields

    @property
    def fields(self: Self) -> list[FilterField]:
        """The list of filter fields for the current object.

        Returns
        -------
        list[FilterField]
            The list of filter fields for the current object.
        """
        return self.__fields
    
    def add_field(self: Self, field: FilterField) -> Filter:
        """Adds a new filter field to the filter and returns a new Filter object.

        Parameters
        ----------
        field : FilterField
            The filter field to be added.

        Returns
        -------
        Filter
            A new Filter object with the added filter field.
        """
        cur_fields = self.fields
        new_fields = cur_fields + [field]
        new_filter = Filter(new_fields)
        return new_filter
