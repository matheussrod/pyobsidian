"""
This module contains the classes that represent Obsidian search strategies.

A search strategy define how [Filter](filter.md) are applied to [Vault](vault.md).

A generic interface for search strategies is provided by the SearchBy class.
"""

from datetime import datetime
from pyobsidian.note import Note
from pyobsidian.filter import Field, FieldKey, FieldValue
import os
import re
from typing import Protocol, Self

class SearchBy(Protocol):
    """Interface for search strategies."""
    def search(self: Self, notes: list[Note], field: Field,) -> list[Note]:
        """Search for notes that match the given field value.

        The implementation is given by the `__search` method.

        Parameters
        ----------
        notes : list[Note]
            A list of notes to search through.
        field : Field
            The field to search for.

        Returns
        -------
        list[Note]
            A list of notes that match the field value.
        """
        ...

    def condition(self: Self, note: Note, field: Field) -> bool:
        """Function that implements the condition of the search.

        Parameters
        ----------
        note : Note
            The note to be checked.
        field : Field
            The field to be checked.

        Returns
        -------
        bool
            True if the condition is met, False otherwise.
        """
        ...

    def __search(self, notes: list[Note], field: Field) -> list[Note]:
        """Mechanism for the search.

        It's used by the `search` method.

        Parameters
        ----------
        notes : list[Note]
            A list of notes to search through.
        field : Field
            The field to search for.

        Returns
        -------
        list[Note]
            A list of notes that match the field value.
        """
        ...

    def is_valid_value(self: Self, value: FieldValue) -> bool:
        """Check if the given value is a valid field value.

        Parameters
        ----------
        value : FieldValue
            The value to be checked.

        Returns
        -------
        bool
            True if the value is valid, False otherwise.

        Raises
        ------
        ValueError
            If the value is not a string or a list.
        """
        ...

    @staticmethod
    def convert_field_value_to_list(value: FieldValue) -> FieldValue:
        """Convert the given field value to a list if it's a string.

        Parameters
        ----------
        value : FieldValue
            The field value to be converted.

        Returns
        -------
        list[str]
            A list of strings.
        """
        ...

class SearchByDefault(SearchBy):
    """Default search strategy. Acts as a template for other search strategies."""
    def is_valid_value(self: Self, value: FieldValue) -> bool:
        """Default check if a string or a list. If not, raise an error.
        
        Returns
        -------
        bool
            True if the value is valid, False otherwise.

        Raises
        ------
        ValueError
            If the value is not a string or a list.
        """
        if not isinstance(value, str) and not isinstance(value, list):
            raise ValueError(f'`{value}` must be a string or a list')
        return True

    def search(
        self: Self, 
        notes: list[Note], 
        field: Field
    ) -> list[Note]:
        self.is_valid_value(field.value)
        filtered_notes = self.__search(notes, field)
        return filtered_notes

    def __search(self, notes: list[Note], field: Field) -> list[Note]:
        """Default search mechanism.
        
        In this mechanism, each value of the field is checked against the
        notes. If the value is found in the note, it is added to the
        filtered notes list.

        A set is used to remove potential duplicates.
        """
        values = self.convert_field_value_to_list(field.value)
        filtered_notes = []
        for value in values:
            cur_field = Field(field.key, value, field.occurrence)
            for note in notes:
                if self.condition(note, cur_field):
                    filtered_notes.append(note)
        return list(set(filtered_notes))

    def condition(self: Self, note: Note, field: Field) -> bool:
        """Default condition check if field value is in the note properties."""
        return field.value in getattr(note.properties, field.key)

    @staticmethod
    def convert_field_value_to_list(value: FieldValue) -> FieldValue:
        if isinstance(value, str):
            return [value]
        else:
            return value

    def __repr__(self: Self) -> str:
        return f'SearchByDefault()'

class SearchByContent(SearchByDefault):
    """Search by note properties content"""
    def __repr__(self: Self) -> str:
        return f'SearchByContent()'

class SearchByFolder(SearchByDefault):
    """Search by note properties folder"""
    def condition(self: Self, note: Note, field: Field) -> bool:
        """Condition check if any value of field value is in the note properties folder."""
        norm_value = os.path.normpath(str(field.value))
        attrs = getattr(note.properties, field.key)
        return any([norm_value in attr for attr in attrs])

    def __repr__(self: Self) -> str:
        return f'SearchByFolder()'
    
class SearchByRegex(SearchByDefault):
    """Search by regex in note properties content"""
    def condition(self: Self, note: Note, field: Field) -> bool:
        """Condition check regex pattern matches in note properties content."""
        attr = getattr(note.properties, 'content')
        return any(re.findall(str(field.value), attr))

    def __repr__(self: Self) -> str:
        return f'SearchByRegex()'

class SearchByDate(SearchByDefault):
    """Search by note properties date"""
    def is_valid_value(self: Self, value: FieldValue) -> bool:
        """Check if the given value is a valid date field value.
        
        Parameters
        ----------
        value : FieldValue
            The value to be checked.

        Returns
        -------
        bool
            True if the value is valid, False otherwise.

        Raises
        ------
        ValueError
            If the value is not a list with 3 elements
        """
        if not isinstance(value, list):
            raise ValueError(f'`{value}` must be a list')
        if len(value) != 3:
            raise ValueError(f'`{value}` must be a list with 3 elements: [\'date_propertie\', \'start_date\', \'end_date\']')
        if isinstance(value, list) and len(value) == 3:
            return True
        raise ValueError(f'`{value}` must be a list with 3 elements: [\'date_propertie\', \'start_date\', \'end_date\']')

    def condition(self: Self, note: Note, field: Field) -> bool:
        """Condition check if note date propertie is between start and end date.
        
        First element from field value is the date propertie.
        Second and third elements from field value are start and end date respectively.

        Parameters
        ----------
        note : Note
            The note to be checked.
        field : Field
            The field to be checked.

        Returns
        -------
        bool
            True if the note date propertie is between start and end date, False otherwise.
        """
        value = field.value
        date_propertie = value[0]
        start_date = datetime.strptime(value[1], '%Y-%m-%d')
        end_date = datetime.strptime(value[2], '%Y-%m-%d')
        note_date = getattr(note.properties, date_propertie)
        return note_date >= start_date and note_date <= end_date
    
    def search(
        self: Self, 
        notes: list[Note], 
        field: Field
    ) -> list[Note]:
        self.is_valid_value(field.value)
        filtered_notes = self.__search(notes, field)
        return filtered_notes
    
    def __search(self, notes: list[Note], field: Field) -> list[Note]:
        """Date search mechanism.
        
        In this mechanism, same logic as the `SearchByDefault` class is used.
        However, the field values ​​are not traversed as the list is passed to the `condition`.

        A set is used to remove potential duplicates.
        """
        filtered_notes = []
        for note in notes:
            if self.condition(note, field):
                filtered_notes.append(note)
        return list(set(filtered_notes))
    
    def __repr__(self: Self) -> str:
        return f'SearchByDate()'

class SearchByOccurrence(SearchByDefault):
    """Occurrence search strategy.
    
    Acts as a template for search strategies that need to check
    if the field value is in the note properties that occurs
    inline, yaml or both.
    """
    def condition(self: Self, note: Note, field: Field) -> bool:
        """Condition check if any value of field value is in the note properties that occurs inline, yaml or both.
        
        Use the same `search` method as the `SearchByDefault` class.
        """
        inline = getattr(note.properties, field.key)['inline']
        yaml = getattr(note.properties, field.key)['yaml']
        check_inline = field.value in inline if inline else False
        check_yaml = field.value in yaml if yaml else False
        match field.occurrence:
            case 'inline':
                return check_inline
            case 'yaml':
                return check_yaml
            case 'file':
                return check_inline or check_yaml
            case _:
                raise ValueError(f'`{field.occurrence}` is not a valid tag occurrence')

    def __repr__(self: Self) -> str:
        return f'SearchByOccurrence()'

class SearchByTag(SearchByOccurrence):
    """Search by note properties tag inline, yaml or both"""
    def __repr__(self: Self) -> str:
        return f'SearchByTag()'
    
class SearchByRelatedNote(SearchByOccurrence):    
    def __repr__(self: Self) -> str:
        return f'SearchByRelatedNote()'

def get_search_strategies() -> dict[FieldKey, SearchBy]:
    """Define a dict of search strategies
    
    Returns
    -------
    dict[FieldKey, SearchBy]
        The dict of search strategies
    """
    return {
        'folder': SearchByFolder(),
        'content': SearchByContent(),
        'regex': SearchByRegex(),
        'date': SearchByDate(),
        'tag': SearchByTag(),
        'related_note': SearchByRelatedNote()
    }
