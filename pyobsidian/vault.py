"""
This module contains the classes that represent Obsidian vaults.

A vault is a collection of notes that can be searched through.
"""

from __future__ import annotations

from pyobsidian.adder import (
    Adder, AdderWhere, AdderField,
    AdderKey, AdderFieldWhere, AdderValue
)
from pyobsidian.adder_op import Op
from pyobsidian.filter import (
    Field, FieldKey, FieldOcurrence, FieldValue,
    Filter, FilterField, FilterMode
)
from pyobsidian.note import Note
from pyobsidian.searchby import get_search_strategies, SearchBy
from pyobsidian.formatter import Formatter
import os
from typing import Literal, Self
import textwrap

class Vault:
    """A class that represents an Obsidian vault.

    Parameters
    ----------
    path : str
        The path of the vault.
    notes : list[Note], optional
        The list of notes in the vault
    filter : Filter, optional
        The filter applied to the vault
    """
    __search_strategies = get_search_strategies()
    __adder_strategies = Adder()

    def __init__(
        self: Self,
        path: str,
        notes: list[Note] = [],
        filter: Filter = Filter(),
        adder: Adder = Adder()
    ) -> None:
        self.__path = path
        self.__notes = notes
        self.__filter = filter
        self.__adder = adder

    @property
    def path(self: Self) -> str:
        """The path of the vault
        
        Returns
        -------
        str
            The path of the vault
        """
        return self.__path
    
    @property
    def notes(self: Self) -> list[Note]:
        """The list of notes in the vault
        
        Returns
        -------
        list[Note]
            The list of notes in the vault
        """
        return self.__notes

    @property
    def filter(self: Self) -> Filter:
        """The filter applied to the vault
        
        Returns
        -------
        Filter
            The filter applied to the vault"""
        return self.__filter
    
    @property
    def adder(self: Self) -> Adder:
        """The adder applied to the vault
        
        Returns
        -------
        Filter
            The adder applied to the vault"""
        return self.__adder

    @property
    def search_strategies(self: Self) -> dict[FieldKey, SearchBy]:
        """The search strategies used by the vault
        
        Returns
        -------
        dict[FieldKey, SearchBy]
            The search strategies used by the vault
        """
        return self.__search_strategies

    @property
    def adder_strategies(self: Self) -> dict[AdderKey, AdderWhere]:
        """The adder strategies used by the vault
        
        Returns
        -------
        dict[AdderKey, AdderWhere]
            The adder strategies used by the vault
        """
        return self.__adder_strategies.registry.where

    @property
    def formatters(self: Self) -> dict[tuple[str, str], Formatter]:
        """The formatters used by the vault
        
        Returns
        -------
        dict[tuple[str, str], Formatter]
            The formatters used by the vault
        """
        return self.__adder_strategies.registry.formatters

    @classmethod
    def add_new_search_strategy(
        cls: type[Self],
        name: FieldKey,
        strategy: SearchBy
    ) -> dict[FieldKey, SearchBy]:
        """Adds a new search strategy to Vault class.

        Parameters
        ----------
        name : FieldKey
            The name of the new search strategy.
        strategy : SearchBy
            The search strategy to be added.

        Returns
        -------
        dict[FieldKey, SearchBy]
            The updated search strategies.
        """
        cls.__search_strategies[name] = strategy
        new_strategy = cls.__search_strategies
        return new_strategy

    @classmethod
    def add_new_adder_strategy(
        cls: type[Self],
        name: AdderKey,
        strategy: AdderWhere
    ) -> dict[str, AdderWhere]:
        """Adds a new adder strategy to Vault class.

        Parameters
        ----------
        name : AdderKey
            The name of the new adder strategy.
        strategy : AdderField
            The adder strategy to be added.

        Returns
        -------
        dict[str, AdderWhere]
            The updated adder strategies.
        """
        cls.__adder_strategies.registry.add_registry(name, strategy)
        return cls.__adder_strategies.registry.where

    @classmethod
    def add_new_formatter(
        cls: type[Self],
        name: str,
        where: str,
        formatter: Formatter
    ) -> dict[tuple[str, str], Formatter]:
        """Adds a new adder formatter to Vault class.

        Parameters
        ----------
        name : AdderKey
            The name of the new adder formatter.
        formatter : AdderField
            The formatter to be added.

        Returns
        -------
        dict[tuple[str, str], Formatter]
            The updated adder formatters.
        """
        cls.__adder_strategies.registry.add_formatter(name, where, formatter)
        return cls.__adder_strategies.registry.formatters

    def get_notes(self: Self, extension: str='.md') -> list[Note]:
        """Retrieves a list of notes from the specified vault directory.

        Parameters
        ----------
        extension : str, optional
            The file extension to filter the notes by. Defaults to '.md'.

        Returns
        -------
        list[Note]
            A list of Note objects representing the notes found in the vault directory.
        """
        root = self.path
        notes = []
        for root, _, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith(extension):
                    note_path = os.path.join(root, filename)
                    notes.append(Note(note_path))
        return notes

    def find_by(
        self: Self, 
        by: FieldKey, 
        value: FieldValue,
        occurrence: FieldOcurrence = 'file',
        mode: FilterMode='and'
    ) -> Vault:
        """Add a new filter field to current filter.

        `by`, `value` and `occurrence` build the field to search for.
        mode is used to specify how the filter should be applied.
        If mode is 'and' (default) the filter will be applied in current vault notes.
        If mode is 'or' the filter will be applied in all vault notes.
        This can be used to create complex filters.
        The sequence of the filter fields will be preserved.
        
        For example vault.find_by('folder', 'folder1').find_by('folder', 'folder2').
        In this case, the filter will be applied to search for notes in folder1.
        After that, the filter will be applied in notes that are returned by first filter, returning notes in folder2.
        This example is equivalent to finding notes that are in 'folder2' which is a subfolder of 'folder1'. 

        If mode is 'or' the filter will be applied to search for notes in folder1 or folder2.

        Parameters
        ----------
        by : FieldKey
            The field to search by.
        value : FieldValue
            The value to search for.
        occurrence : FieldOcurrence, optional
            The occurrence of the value to search for. Defaults to 'file'.
        mode : FilterMode, optional
            The mode of the filter. Defaults to 'and'.
        
        Returns
        -------
        Vault
            A new Vault object with the new filter field added.
        """
        field = Field(by, value, occurrence)
        filter_field = FilterField(field, mode)
        cur_filter = self.filter
        new_filter = cur_filter.add_field(filter_field)
        new_vault = Vault(path=self.path, notes=self.notes, filter=new_filter)
        return new_vault
    
    def add(
        self: Self, 
        by: AdderKey, 
        value: AdderValue,
        where: Literal['inline', 'yaml'] | Op
    ) -> Vault:
        """Add a new adder field to current adder.

        `by`, `value` and `where` build the field to add.
        
        - by is used to find which AdderWhere to add to.
        - value is the value to add.
        - where is the where to add the value: inline, yaml or an Op.

        Parameters
        ----------
        by : AdderKey
            The field to add by.
        value : AdderValue
            The value to add.
        where : Literal['inline', 'yaml'] | Op
            The where to add the field.
        
        Returns
        -------
        Vault
            A new Vault object with the new adder field added.
        """
        if isinstance(where, Op):
            adder_field = AdderField(by, value, (where.id, where))
        else:
            adder_field = AdderField(by, value, where)
        cur_adder = self.adder
        new_adder = cur_adder.add_field(adder_field)
        new_vault = Vault(path=self.path, notes=self.notes, filter=self.filter, adder=new_adder)
        return new_vault

    def __search(
        self,
        notes: list[Note], 
        field: Field
    ) -> list[Note]:
        """A function that searches for notes based on a given field using a specific search strategy.

        Parameters
        ----------
        notes : list[Note]
            A list of notes to search through.
        field : Field
            The field to search for.

        Returns
        -------
        list[Note]
            A list of notes that match the search criteria.
        """
        search_strategy = self.search_strategies[field.key]
        notes = search_strategy.search(notes, field)
        return notes
    
    def execute(self: Self) -> Vault:        
        """This method applies the filter and adder to the current Vault object.

        First, all filter fields are applied. Then, all adder fields are applied.

        Returns
        -------
        Vault
            A new Vault object with the filter applied.
        """
        filter = self.filter
        if not filter:
            return self
        notes = self.notes
        if not notes:
            notes = self.get_notes()
    
        filtered_notes = notes
        new_notes: list[Note] = []
        for f_field in filter:
            mode = f_field.mode
            if mode == 'and':
                new_notes = self.__search(new_notes or filtered_notes, f_field.field)
            elif mode == 'or':
                new_notes.extend(self.__search(notes, f_field.field))
            else:
                raise ValueError(f'`{mode}` is not a valid mode. Must be `and` or `or`')
        unique_new_notes = list(set(new_notes))

        adder = self.adder
        if not adder:
            return Vault(path=self.path, notes=unique_new_notes, filter=filter, adder=Adder())
        for note in unique_new_notes:
            for add in adder:
                key = add.key
                value = add.value
                where = add.where
                formatter = adder.registry.get_formatter(key, where)
                adder_where = adder.registry.get_where(where)
                if adder_where is None:
                    message = textwrap.dedent(f"""
                        Invalid where: '{where}' in `.add('{key}', {value}, '{where}')`
                        Checking in {adder.registry.where} I found {list(adder.registry.where.keys())}.
                        Hints:
                            - Check that you haven't made any typing errors.
                            - Check if AdderWhere implementation exists.
                            - If you don't find it, add new adder strategy.
                                - To do this, implement your own AdderWhere.
                                - Use Vault.add_new_adder_strategy()
                    """)
                    raise ValueError(message)
                if formatter is None:
                    message = textwrap.dedent(f"""
                        Invalid formatter: "{(key, where)}" in `.add('{key}', {value}, '{where}')`
                        Checking in {adder.registry.formatters} I found {list(adder.registry.formatters.keys())}.
                        I need a Formatter to format the value because this operation will modify the content of the note.
                        In your case, you need to implement at least a Formatter for '{key}' with '{where}'.
                        Hints:
                            - Check that you haven't made any typing errors.
                            - Check if Formatter implementation exists.
                            - If you don't find it, add new formatter.
                                - To do this, implement your own Formatter. 
                                - Use Vault.add_new_adder_formatter()
                    """)
                    raise ValueError(message)
                new_value = formatter.format(value)
                new_field = AdderField(key, new_value, where)
                new_content = adder_where.exec(note, new_field)
                if new_content is None:
                    continue
                note.properties.content = new_content
            note.write()
        return Vault(path=self.path, notes=unique_new_notes, filter=filter, adder=Adder())
    
    def __repr__(self) -> str:
        return f"Vault('{self.path}', {self.notes}, {self.filter}, {self.adder})"
