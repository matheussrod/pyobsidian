
from datetime import datetime, timedelta
from pyobsidian.searchby import (
    SearchByDefault,
    SearchByFolder,
    SearchByRegex,
    SearchByDate,
    SearchByOccurrence
)
from pyobsidian.filter import Field
import pytest

# SearchByDefault ------------------------------------------------------------
def test_searchby_default_convert_field_value_to_list_str():
    search_by = SearchByDefault()
    value = 'folder'
    assert search_by.convert_field_value_to_list(value) == [value]

def test_searchby_default_convert_field_value_to_list_list():
    search_by = SearchByDefault()
    value = ['folder']
    assert search_by.convert_field_value_to_list(value) == value

def test_searchby_default_is_valid_value_valid_value():
    search_by = SearchByDefault()
    valid_value = 'folder'
    assert search_by.is_valid_value(valid_value)

def test_searchby_default_is_valid_value_invalid_value():
    search_by = SearchByDefault()
    valid_value = None
    with pytest.raises(ValueError):
        search_by.is_valid_value(valid_value)

def test_searchby_default_condition_true(note):
    search_by = SearchByDefault()
    field = Field('content', 'testing', 'file')
    assert search_by.condition(note, field)

def test_searchby_default_condition_false(note):
    search_by = SearchByDefault()
    field = Field('content', 'invalid', 'file')
    assert not search_by.condition(note, field)

def test_searchby_default_search_empty_notes():
    search_by = SearchByDefault()
    notes = []
    field = Field('folder', 'value', 'file')
    assert search_by.search(notes, field) == []

def test_searchby_default_search_non_empty_notes_with_valid_search(note):
    search_by = SearchByDefault()
    field = Field('content', 'testing', 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_default_search_non_empty_notes_with_invalid_search(note):
    search_by = SearchByDefault()
    field = Field('content', 'invalid', 'file')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_folder_search_empty_notes():
    search_by = SearchByFolder()
    notes = []
    field = Field('folder', 'value', 'file')
    assert search_by.search(notes, field) == []

def test_searchby_folder_search_non_empty_notes_with_valid_search(note):
    search_by = SearchByFolder()
    field = Field('folder', note.properties.folder[-1], 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_folder_search_non_empty_notes_with_invalid_search(note):
    search_by = SearchByFolder()
    field = Field('folder', 'invalid', 'file')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_folder_search_non_empty_notes_with_one_valid_search(note):
    search_by = SearchByFolder()
    field = Field('folder', [note.properties.folder[-1], 'invalid'], 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_regex_empty_notes():
    search_by = SearchByRegex()
    notes = []
    field = Field('content', 'value', 'file')
    assert search_by.search(notes, field) == []

def test_searchby_regex_non_empty_notes_with_valid_search(note):
    search_by = SearchByRegex()
    field = Field('content', r'\{\{[a-zA-Z0-9]*\}\}', 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_regex_non_empty_notes_with_invalid_search(note):
    search_by = SearchByRegex()
    field = Field('content', 'invalid', 'file')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_date_valid_value_valid_value():
    search_by = SearchByDate()
    valid_value = ['date', '2024-01-01', '2024-01-01']
    assert search_by.is_valid_value(valid_value)

def test_searchby_date_valid_value_invalid_value():
    search_by = SearchByDate()
    valid_value = 'invalid'
    with pytest.raises(ValueError):
        search_by.is_valid_value(valid_value)

def test_searchby_date_condition_true(note):
    note.write()
    search_by = SearchByDate()
    today = datetime.today().strftime('%Y-%m-%d')
    field = Field('date', ['creation_time', today, '9999-01-01'], 'file')
    assert search_by.condition(note, field)

def test_searchby_date_condition_false(note):
    note.write()
    search_by = SearchByDate()
    today = datetime.today().strftime('%Y-%m-%d')
    field = Field('date', ['creation_time', '1970-01-01', today], 'file')
    assert not search_by.condition(note, field)

def test_searchby_date_search_empty_notes():
    search_by = SearchByDate()
    notes = []
    field = Field('date', ['creation_time', '1970-01-01', '9999-01-01'], 'file')
    assert search_by.search(notes, field) == []

def test_searchby_date_search_non_empty_notes_with_valid_search(note):
    note.write()
    search_by = SearchByDate()
    field = Field('date', ['creation_time', '1970-01-01', '9999-01-01'], 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_date_search_non_empty_notes_with_invalid_search(note):
    note.write()
    search_by = SearchByDate()
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    field = Field('date', ['creation_time', tomorrow, '9999-01-01'], 'file')
    notes = [note]
    assert search_by.search(notes, field) == []

# SearchByOccurrence ---------------------------------------------------------
def test_searchby_occurrence_search_empty_notes():
    search_by = SearchByOccurrence()
    notes = []
    field = Field('content', 'value', 'file')
    assert search_by.search(notes, field) == []

def test_searchby_occurrence_search_non_empty_notes_with_valid_yaml_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'test', 'yaml')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_occurrence_search_non_empty_notes_with_invalid_yaml_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'invalid', 'yaml')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_occurrence_search_non_empty_notes_with_valid_inline_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'tag1', 'inline')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_occurrence_search_non_empty_notes_with_invalid_inline_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'invalid', 'inline')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_occurrence_search_non_empty_notes_with_valid_file_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'tag1', 'file')
    notes = [note]
    assert search_by.search(notes, field) == notes

def test_searchby_occurrence_search_non_empty_notes_with_invalid_file_search(note):
    search_by = SearchByOccurrence()
    field = Field('tag', 'invalid', 'file')
    notes = [note]
    assert search_by.search(notes, field) == []

def test_searchby_occurrence_raises_error_when_field_is_invalid(note):
    search_by = SearchByOccurrence()
    field = Field('tag', ['tag1', 'tag2'], 'invalid')
    notes = [note]
    with pytest.raises(ValueError):
        search_by.search(notes, field)
