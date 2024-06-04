"""
This module contains the classes that represent adders.

Adders are used to add content to Obsidian notes.
"""

from __future__ import annotations

import copy as cp
from dataclasses import dataclass
from pyobsidian.adder_op import Op
from pyobsidian.formatter import *
from pyobsidian.helpers import convert_str_or_list_to_list, has_yaml
from pyobsidian.markdown import MkHeaderLevels
from pyobsidian.note import Note
import re
import textwrap
from typing import Iterator, Literal, Optional, Protocol, Self, Type
import warnings
import yaml

AdderKey = str
AdderValue = str | list[str]
AdderFieldWhere = Literal['inline', 'yaml'] | tuple[str, Op]

@dataclass
class AdderField:
    """Class that represents an adder field."""
    key: AdderKey
    value: AdderValue
    where: AdderFieldWhere

class AdderWhere(Protocol):
    """Interface for adder where."""
    def exec(
        self: Self, 
        note: Note,
        field: AdderField
    ) -> Optional[str]:
        """Execute the adder where.

        Parameters
        ----------
        note : Note
            The note to add the content to.
        field : AdderField
            The field to add the content to.

        Returns
        -------
        Optional[str]
            The content to add to the note.
        """
        ...

class AdderWhereInline(AdderWhere):
    """Class that represents an adder where inline."""
    def __repr__(self: Self) -> str:
        return 'AdderWhereInline()'
    
    def exec(
        self: Self, 
        note: Note,
        field: AdderField
    ) -> str:
        content = note.properties.content
        if has_yaml(content):
            new_content = f'\n---\n{field.value}'
            new_note_content = re.sub(
                r'(?<=)\n(---\n)',
                new_content,
                content
            )
            return new_note_content
        else:
            new_content = f'{field.value}'
            new_note_content = new_content + content
            return new_note_content

class AdderWhereYaml(AdderWhere):
    """Class that represents an adder where yaml."""
    def __repr__(self: Self) -> str:
        return 'AdderWhereYaml()'
    
    def exec(
        self: Self, 
        note: Note,
        field: AdderField
    ) -> str:
        content = note.properties.content
        note_yaml = cp.deepcopy(note.properties.yaml_content)
        key = field.key
        # Since Obsidian 1.4.
        # https://help.obsidian.md/Editing+and+formatting/Properties#Default+properties
        deprecated_properties = {
            'tag': 'tags',
            'alias': 'aliases',
            'cssclass': 'cssclasses'
        }
        if key in deprecated_properties:
            key = deprecated_properties[key]
        value = convert_str_or_list_to_list(field.value)
        if note_yaml is None:
            note_yaml = {key: value}
            new_yaml = '---\n' + yaml.dump(note_yaml) + '---\n\n'
            new_note_content = new_yaml + content
            return new_note_content
        elif note_yaml.get(key) is None:
            note_yaml[key] = value
        elif isinstance(note_yaml[key], str):
            note_yaml[key] = list(set(convert_str_or_list_to_list(note_yaml[key]) + value))
        else:
            note_yaml[key] = list(set(note_yaml[key] + value))
        new_note_yaml = yaml.dump(note_yaml)
        new_note_content = re.sub(
            r'(?<=---\n)(.*)(?=---\n)', 
            new_note_yaml,
            content, 
            flags=re.DOTALL
        )
        return new_note_content

class AdderWhereOpMkHeader(AdderWhere):
    """Class that represents an adder where op mk header."""
    def __repr__(self: Self) -> str:
        return 'AdderWhereOpMkHeader()'
    
    def exec(
        self: Self, 
        note: Note,
        field: AdderField
    ) -> Optional[str]:
        content = note.properties.content
        where = field.where
        value = field.value

        if isinstance(where, tuple):
            op = where[1]
        else:
            message = textwrap.dedent(f"""
                The method `exec` in AdderWhereOpMkHeader expected a tuple in where argument.
                I extract it from {field}.
                You need to give me a tuple[str, Op]
            """)
            raise ValueError(message)

        if not isinstance(op, Op):
            message = textwrap.dedent(f"""
                I expect an Op in second element of where {where}.
                You gave me: '{op}'
            """)
            raise ValueError(message)

        levels = MkHeaderLevels(content).get_levels()
        if levels == dict():
            message = textwrap.dedent(f"""
                There is no header in '{note.path}'.
                I will ignore this operator: {op}
            """)
            warnings.warn(message)
            return None
        operator = op.operator
        precedence = operator['precedence']
        level = str(operator['level'])
        index = int(operator['index']) - 1
        h_level = levels.get(level)
        if h_level is None or index >= len(h_level):
            message = textwrap.dedent(f"""
                The operator {op} does not match any header level in '{note.path}'.
                I will ignore this operator. The header levels I have in this note are:
                {levels}
            """)
            warnings.warn(message)
            return None
    
        content_adj = f'{value}'
        hl_index = h_level[index]
        h_start = int(hl_index['start'])
        h_end = int(hl_index['end'])
        if precedence == '<|':    
            #content_start = content[:h_start - 1]
            #content_end = content[h_start:]
            content_start = content[:h_start]
            content_end = content[h_start:]
        elif precedence == '|>':
            content_start = content[:h_end]
            content_end = content[h_end + 1:]
        new_content = content_start + content_adj + content_end
        return new_content

class AdderRegistry:
    """Adder registry.
    
    Consolidates AdderWhere along with its possible formatters.
    T"""
    where = {
        'inline': AdderWhereInline(),
        'yaml': AdderWhereYaml(),
        'mkheader': AdderWhereOpMkHeader()
    }

    formatters = {
        ('tag', 'yaml'): FormatterTagYaml(),
        ('tag', 'inline'): FormatterTagInline(),
        ('tag', 'mkheader'): FormatterTagOpMkHeader(),
        ('content', 'yaml'): FormatterContentYaml(),
        ('content', 'inline'): FormatterContentInline(),
        ('content', 'mkheader'): FormatterContentOpMkHeader(),
        ('related_note', 'yaml'): FormatterRelatedNoteYaml(),
        ('related_note', 'inline'): FormatterRelatedNoteInline(),
        ('related_note', 'mkheader'): FormatterRelatedNoteOpMkHeader()
    }

    @classmethod
    def get_where(cls: Type, key: str | tuple) -> Optional[AdderWhere]:
        """Get the adder where.

        Parameters
        ----------
        key : str
            The key of the where.
        """
        if isinstance(key, tuple):
            return cls.where.get(key[0])
        return cls.where.get(key)

    @classmethod
    def add_registry(cls: Type, key: str, where: AdderWhere) -> dict[str, AdderWhere]:
        """Add a new where to the registry.

        Parameters
        ----------
        key : str
            The key of the where.
        where : AdderWhere
            The where to add.
        """
        cls.where[key] = where
        return cls.where
    
    @classmethod
    def get_formatter(
        cls: Type, 
        by: str, 
        where: AdderFieldWhere
    ) -> Optional[Formatter]:
        """Get the adder formatter.

        Parameters
        ----------
        by : str
            The key of the formatter.
        where : AdderFieldWhere
            The where of the formatter.

        Returns
        -------
        Optional[Formatter]
            The formatter.
        """
        if isinstance(where, tuple):
            return cls.formatters.get((by, where[0]))
        return cls.formatters.get((by, where))
    
    @classmethod
    def add_formatter(
        cls: Type, 
        by: str, 
        where: str, 
        formatter: Formatter
    ) -> dict[tuple[str, str], Formatter]:
        """Add a new adder formatter to Adder class.

        Parameters
        ----------
        by : str
            The key of the formatter.
        where : str
            The where of the formatter.
        formatter : Formatter
            The formatter to be added.

        Returns
        -------
        dict[tuple[str, str], Formatter]
            The updated formatters.
        """
        cls.formatters[(by, where)] = formatter
        return cls.formatters

class Adder:
    """Adder class.

    Parameters
    ----------
    fields : list[AdderField]
        The fields of the adder.

    """
    __registry: AdderRegistry = AdderRegistry()

    def __init__(self: Self, fields: list[AdderField] = []) -> None:
        self.__fields = fields

    def __repr__(self: Self) -> str:
        return f"Adder({self.fields})"

    def __iter__(self: Self) -> Iterator[AdderField]:
        for field in self.fields:
            yield field

    def __len__(self: Self):
        return len(self.fields)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Adder):
            return False
        return self.fields == value.fields

    @property
    def registry(self: Self) -> AdderRegistry:
        return self.__registry

    @property
    def fields(self: Self) -> list[AdderField]:
        return self.__fields

    def add_field(self: Self, field: AdderField) -> Adder:
        """Add a new adder field to the adder.

        Parameters
        ----------
        field : AdderField
            The field to be added.

        Returns
        -------
        Adder
            The new adder.
        """
        cur_fields = self.fields
        new_fields = cur_fields + [field]
        new_adder = Adder(new_fields)
        return new_adder
