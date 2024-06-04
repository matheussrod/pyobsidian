"""
This module contains the classes that represent Obsidian notes.
It provides classes for reading, writing, and retrieving properties of Obsidian notes.
"""

from __future__ import annotations

from datetime import datetime
from itertools import accumulate
from pyobsidian.helpers import read_file
import os
import re
from typing import Optional, Self
import yaml

class NoteProperties:
    """A class used to retrieve properties of Obsidian notes.

    Parameters
    ----------
    path : str
        The path of the note file
    content : str
        The content of the note file
    """
    def __init__(self: Self, path: str, content: str):
        self.__path = path
        self.__content = content

    def __repr__(self: Self) -> str:
        return f"NoteProperties(path='{self.path}', content='{self.content}')"

    def _get_yaml_field(self: Self, field: str) -> Optional[str | list[str]]:
        """Retrieves the value of a specified field from the YAML content of the note.

        Parameters
        ----------
        field : str
            The name of the field to retrieve the value of.

        Returns
        -------
        Optional[str | list[str]]
            The value of the specified field if it exists in the YAML content, 
            otherwise None.
        """
        if self.yaml_content is None:
            return None
        field_value = self.yaml_content.get(field)
        return field_value

    def _get_tags_yaml(self: Self) -> Optional[list[str]]:
        """Retrieves the tags from the YAML content of the note.

        Returns
        -------
        Optional[list[str]]
            The list of tags if they exist in the YAML content, 
            otherwise None.
        """
        yaml_tags = self._get_yaml_field('tags')
        if isinstance(yaml_tags, str):
            yaml_tags = [yaml_tags]
        return yaml_tags

    def _get_tags_inline(self: Self) -> Optional[list[str]]:
        """Retrieves all the inline tags from the content of the note.

        This function uses regular expressions to find all occurrences of tags in the content of the note.
        The tags are identified by the pattern '#tag', where 'tag' is any non-whitespace sequence of characters.

        Returns
        -------
        Optional[list[str]]
            A list of tags found in the content, or None if no tags are found.
        """
        tags = re.compile(r'#([^\s]+)')
        tags_content = tags.findall(self.content)
        if len(tags_content) == 0:
            return None
        return tags_content

    def _get_related_notes_inline(self: Self) -> Optional[list[str]]:
        """Retrieves all the related notes that are inline in the content of the note.

        This function uses regular expressions to find all occurrences of related notes in the content of the note.
        The related notes are identified by the pattern [[note|alias]], where 'note' is the name of the related note and 'alias' is an optional alias for the note.
        The function removes the alias from the related note and returns a list of the related notes without aliases.

        Returns
        -------
        Optional[list[str]]
            A list of related notes found in the content, without aliases, or None if no related notes are found.
        """
        re_compile = re.compile(r'---(.*?)---', re.DOTALL)
        raw_content = re.sub(re_compile, '', self.content)
        regex = re.compile(r'\[\[(.*?)\]\]')
        related_notes = regex.findall(raw_content)
        if len(related_notes) == 0:
            return None
        related_notes_without_alias = [
            note.split('|')[0] 
            for note in related_notes
        ]
        return related_notes_without_alias

    def _get_related_notes_yaml(self: Self) -> Optional[ dict[str, list[str]] ]:
        """Retrieves related notes from YAML content.

        This function searches for related notes in the YAML content of the note.
        It uses regular expressions to find all occurrences of related notes in the YAML content.
        The related notes are identified by the pattern [[note|alias]], where 'note' is the name of the related note and 'alias' is an optional alias for the note.
        The function removes the alias from the related note and returns a dictionary of the related notes, grouped by the YAML key.

        Returns
        -------
        Optional[dict[str, list[str]]]
            A dictionary of related notes found in the YAML content, grouped by the YAML key, or None if no related notes are found.
        """
        yaml_content = self.yaml_content
        if yaml_content is None:
            return None

        def rec_search(values, compile: re.Pattern = re.compile(r'\[\[(.*?)\]\]')) -> list[str]:
            results = []
            if isinstance(values, str):
                related_notes = re.findall(compile, values)
                related_notes_without_alias = [
                    note.split('|')[0] 
                    for note in related_notes
                ]
                results.extend(related_notes_without_alias)
            elif isinstance(values, list):
                for value in values:
                    results.extend(rec_search(value))
            return results

        related_notes = {}
        for key, values in yaml_content.items():
            related_notes[key] = rec_search(values)
        
        valid_related_notes = {
            key: values
            for key, values in related_notes.items()
            if len(values) > 0
        }
        if len(valid_related_notes) == 0:
            return None
        return valid_related_notes

    @property
    def path(self: Self) -> str:
        """The path of the note file
        
        Returns
        -------
        str
            The path of the note file
        """
        return self.__path
    
    @property
    def content(self: Self) -> str:
        """The content of the note file
        
        Returns
        -------
        str
            The content of the note file
        """
        return self.__content
    
    @content.setter
    def content(self: Self, content: str) -> None:
        """Sets the content of the note file

        Parameters
        ----------
        content : str
            The content of the note file
        """
        self.__content = content
    
    @property
    def filename(self: Self) -> str:
        """Returns the filename of the current object's path.

        This property takes the path of the current object and splits it using the operating system's
        path separator. It then extracts the last element of the resulting list, which represents the
        filename. The filename is further split using the dot separator to remove the file extension.
        The function then returns the extracted filename as a string.

        Returns
        -------
        str
            Note filename.
        """
        path_splited = self.path.split(os.sep)
        filename = path_splited[-1].split('.')[0]
        return filename

    @property
    def last_access_time(self: Self) -> datetime:
        """Retrieves the last access time of the file.

        Notes
        -----
        It uses the `os.path.getatime` function to retrieve the last access time of the file.

        Returns
        -------
        datetime
            The last access time of the file.
        """
        atime = os.path.getatime(self.path)
        atime_datetime = datetime.fromtimestamp(atime)
        return atime_datetime
    
    @property
    def last_modification_time(self: Self) -> datetime:
        """Retrieves the last modification time of the file.

        Notes
        -----
        It uses the `os.path.getmtime` function to retrieve the last modification time of the file.

        Returns
        -------
        datetime
            The last modification time of the file.
        """
        mtime = os.path.getmtime(self.path)
        mtime_datetime = datetime.fromtimestamp(mtime)
        return mtime_datetime
    
    @property
    def creation_time(self: Self) -> datetime:
        """Retrieves the creation time of the note file.

        Notes
        -----
        It uses the `os.path.getctime` function to retrieve the creation time of the file.

        Returns
        -------
        datetime
            The creation time of the note file.
        """
        ctime = os.path.getctime(self.path)
        ctime_datetime = datetime.fromtimestamp(ctime)
        return ctime_datetime

    @property
    def folder(self: Self) -> list[str]:
        """Retrieves the folders path of the current note as a list of strings.
        All combinations of the folder path are returned.
        For example, if the folder path is "C:/Users/user/vault", it returns ['C:', 'C:/Users', 'C:/Users/user', 'C:/Users/user/vault']

        Returns
        -------
        list[str]
            A list containing the folders path of the current note.
        """
        sep = os.sep
        folder, _ = os.path.split(self.path)
        folders = list(accumulate(
            func=lambda x, y: os.path.join(x, y),
            iterable=folder.split(sep)
        ))
        return folders

    @property
    def yaml_content(self: Self) -> Optional[dict]:
        """Retrieves the YAML content from the note.
        The YAML is identified by '---'.
        All text between these two delimiters is considered part of the YAML content.
        If more than one '---' separator is found, only the first pair is considered.

        Notes
        -----
        See [Obsidian properties](https://help.obsidian.md/Editing+and+formatting/Properties) for more details.
        
        Returns
        -------
        Optional[dict]
            The YAML content of the note, or None if no YAML content is found.
        """
        re_compile = re.compile(r'---(.*?)---', re.DOTALL)
        re_findall = re.findall(re_compile, self.content)
        if len(re_findall) == 0:
            return None
        first_yaml = re_findall[0]
        try:
            yaml_content = yaml.safe_load(first_yaml)
            return yaml_content
        except yaml.constructor.ConstructorError as e:
            print(f'Error parsing YAML in {self.path}')
            raise e
    
    @property
    def tag(self: Self) -> dict[str, Optional[list[str]]]:
        """Retrieves the tags from the note.

        This property returns a dictionary containing the tags extracted from the note.
        The dictionary has two keys:

        - 'yaml': The tags extracted from the YAML content of the note. It is a list of strings or None if no tags are found.
        - 'inline': The tags extracted from the inline content of the note. It is a list of strings or None if no tags are found.

        Returns
        -------
        dict[str, Optional[list[str]]]
            A dictionary containing the tags extracted from the note.
        """
        inline_tags = self._get_tags_inline()
        yaml_tags = self._get_tags_yaml()
        tags = {
            'yaml': yaml_tags,
            'inline': inline_tags
        }
        return tags

    @property
    def related_note(self: Self) -> dict[
        str, 
          Optional[list[str]]
        | Optional[dict[str, list[str]]]
    ]:
        """Retrieves related notes from both YAML content and inline content.

        This property returns a dictionary containing the related notes extracted from both the YAML content and inline content of the note.
        The dictionary has two keys:
        - 'yaml': The related notes extracted from the YAML content of the note. It is a dictionary where the keys are the YAML keys and the values are lists of related note names.
        - 'inline': The related notes extracted from the inline content of the note. It is a list of related note names.

        Returns
        -------
        dict[str, Union[list[str], dict[str, list[str]]]]
            A dictionary containing the related notes extracted from both the YAML content and inline content of the note.
        """
        inline_related_notes = self._get_related_notes_inline()
        yaml_related_notes = self._get_related_notes_yaml()
        related_notes = {
            'yaml': yaml_related_notes,
            'inline': inline_related_notes
        }
        return related_notes


class Note:
    """Represents a note in Obsidian vault.

    Parameters
    ----------
    path : str
        The path of the note.
    content : str, optional
        The content of the note. If not provided, it will be read from the note file.
    """
    def __init__(self: Self, path: str, content: Optional[str] = None):
        if content is None:
            content = read_file(path)
        self.__path = path
        self.__properties = NoteProperties(path, content)
    
    def __repr__(self) -> str:
        return f"Note(path='{self.path}')"

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, Note):
            return False
        return self.path == other.path
    
    def __hash__(self) -> int:
        return hash(self.path)

    @property
    def path(self: Self) -> str:
        """Retrieves the normalized path of the note.

        Returns
        -------
        str
            The normalized path of the note.
        """
        return os.path.normpath(self.__path)

    @property
    def properties(self: Self) -> NoteProperties:
        """Retrieves the properties of the note.

        Returns
        -------
        NoteProperties
            The properties of the note.
        """
        return self.__properties
    
    def read(self: Self) -> str:
        """Reads the content of a note from the file.

        Returns
        -------
        str
            The content of the note file
        """
        return read_file(self.path)

    def write(self: Self) -> str:
        """Writes the content of a note to the file.

        Returns
        -------
        str
            The path of the written note
        """
        with open(self.path, 'w', encoding='utf8') as file:
            file.write(self.properties.content)
        return self.path

