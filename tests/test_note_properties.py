
from pyobsidian.note import NoteProperties
import os
import pytest
import yaml

def test_get_yaml_field():
    content = """
    ---
    title: Sample Note
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    yaml_field = note_properties._get_yaml_field('title')
    expected_yaml = 'Sample Note'
    assert yaml_field == expected_yaml

def test_get_invalid_yaml_field_raise_constructor_error(invalid_yaml_content):
    with pytest.raises(yaml.constructor.ConstructorError):
        NoteProperties('', invalid_yaml_content).yaml_content

def test_get_yaml_field_without_yaml():
    content = """
    Some content
    """
    note_properties = NoteProperties('', content)
    yaml_field = note_properties._get_yaml_field('title')
    expected_yaml = None
    assert yaml_field == expected_yaml

def test_get_yaml_field_with_missing_field():
    content = """
    ---
    title: Sample Note
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    yaml_field = note_properties._get_yaml_field('tags')
    expected_yaml = None
    assert yaml_field == expected_yaml

def test_get_tags_yaml_with_yaml_tags():
    content = """
    ---
    tags: [tag1, tag2]
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_yaml()
    expected_tags = ['tag1', 'tag2']
    assert note_tags == expected_tags

def test_get_tags_yaml_with_one_yaml_tag():
    content = """
    ---
    tags: tag1
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_yaml()
    expected_tags = ['tag1']
    assert note_tags == expected_tags

def test_get_yaml_tag_with_yaml_but_without_yaml_tag_field():
    content = """
    ---
    title: Sample Note
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_yaml()
    expected_tags = None
    assert note_tags == expected_tags

def test_get_yaml_tag_with_yaml_tag_field_but_without_tags():
    content = """
    ---
    title: Sample Note
    tags: []
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_yaml()
    expected_tags = []
    assert note_tags == expected_tags

def test_get_tags_inline_with_inline_tags():
    content = """
    Some content
    Inline tags: #tag1 #tag2
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_inline()
    expected_tags = ['tag1', 'tag2']
    assert note_tags == expected_tags

def test_get_tags_inline_with_one_inline_tag():
    content = """
    Some content
    Inline tags: #tag1
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_inline()
    expected_tags = ['tag1']
    assert note_tags == expected_tags

def test_get_tags_inline_without_inline_tags():
    content = """
    Some content
    Without inline tags
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_inline()
    expected_tags = None
    assert note_tags == expected_tags

def test_get_tags_inline_with_yaml_tags():
    content = """
    ---
    tags: [tag1, tag2]
    ---
    Some content
    Inline tags #tag3 #tag4
    """
    note_properties = NoteProperties('', content)
    note_tags = note_properties._get_tags_inline()
    expected_tags = ['tag3', 'tag4']
    assert note_tags == expected_tags

def test_get_related_notes_inline():
    content = """
    Some content
    Inline related notes: [[note1]] [[note2]]
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_inline()
    expected_related_notes = ['note1', 'note2']
    assert related_notes == expected_related_notes

def test_get_related_notes_inline_without_inline_related_notes():
    content = """
    Some content
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_inline()
    expected_related_notes = None
    assert related_notes == expected_related_notes

def test_get_related_notes_inline_with_alias():
    content = """
    Some content
    Inline related notes: [[note1|alias1]] [[note2|alias2]]
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_inline()
    expected_related_notes = ['note1', 'note2']
    assert related_notes == expected_related_notes

def test_get_related_notes_inline_with_yaml_related_notes():
    content = """
    ---
    related_notes: [note1, note2]
    ---
    Some content
    Inline related notes: [[note3]] [[note4]]
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_inline()
    expected_related_notes = ['note3', 'note4']
    assert related_notes == expected_related_notes

def test_get_related_notes_yaml():
    content = """
    ---
    related_notes: [note1, note2]
    notes: 
      - "[[note3]]" 
      - "[[note4]]"
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_yaml()
    expected_related_notes = {
        'notes': ['note3', 'note4']
    }
    assert related_notes == expected_related_notes

def test_get_related_notes_yaml_without_yaml():
    content = """
    Some content
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_yaml()
    expected_related_notes = None
    assert related_notes == expected_related_notes

def test_get_related_notes_yaml_with_yaml_without_related_notes():
    content = """
    ---
    title: Sample Note
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_yaml()
    expected_related_notes = None
    assert related_notes == expected_related_notes

def test_get_related_notes_yaml_with_alias():
    content = """
    ---
    title: Sample Note
    related_notes: ["[[note1|alias1]]", "[[note2|alias2]]"]
    ---
    Some content
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties._get_related_notes_yaml()
    expected_related_notes = {
        'related_notes': ['note1', 'note2']
    }
    assert related_notes == expected_related_notes

def test_propertie_filename():
    path = os.path.join('C:' + os.sep, 'Users', 'user', 'vault', 'note.md')
    note_properties = NoteProperties(path=path, content='')
    note_filename = note_properties.filename
    expected_filename = 'note'
    assert note_filename == expected_filename

def test_propertie_last_access_time(note_reader):
    path = note_reader.path
    content = note_reader.read()
    note_properties = NoteProperties(path=path, content=content)
    last_access_time = note_properties.last_access_time
    assert last_access_time is not None

def test_propertie_last_modification_time(note_reader):
    path = note_reader.path
    content = note_reader.read()
    note_properties = NoteProperties(path=path, content=content)
    last_modification_time = note_properties.last_modification_time
    assert last_modification_time is not None

def test_propertie_creation_time(note_reader):
    path = note_reader.path
    content = note_reader.read()
    note_properties = NoteProperties(path=path, content=content)
    creation_time = note_properties.creation_time
    assert creation_time is not None

def test_propertie_folder():
    path = os.path.join('C:' + os.sep, 'Users', 'user', 'vault', 'note.md')
    note_properties = NoteProperties(path=path, content='')
    note_folders = note_properties.folder
    expected_folders = [
        'C:',
        os.path.join('C:', 'Users'),
        os.path.join('C:', 'Users', 'user'),
        os.path.join('C:', 'Users', 'user', 'vault')
    ]
    assert note_folders == expected_folders

def test_propertie_yaml_content():
    content = """
    ---
    title: Sample Note
    tags: [test, sample]
    date: '[[{{date}}]]'
    ---
    Some content
    Inline tags: #tag1 #tag2
    """
    note_properties = NoteProperties('', content)
    yaml_content = note_properties.yaml_content
    expected_yaml = {
        'title': 'Sample Note',
        'tags': ['test', 'sample'],
        'date': '[[{{date}}]]'
    }
    assert yaml_content == expected_yaml

def test_propertie_yaml_content_without_yaml():
    content = """
    Some content
    """
    note_properties = NoteProperties('', content)
    yaml_content = note_properties.yaml_content
    expected_yaml = None
    assert yaml_content == expected_yaml

def test_propertie_tags():
    content = """
    ---
    title: Sample Note
    tags: [tag1, tag2]
    ---
    Some content
    Inline tags: #tag3 #tag4
    """
    note_properties = NoteProperties('', content)
    tags = note_properties.tag
    expected_tags = {
        'yaml': ['tag1', 'tag2'],
        'inline': ['tag3', 'tag4']
    }
    assert tags == expected_tags

def test_propertie_related_notes():
    content = """
    ---
    title: "[[Sample Note|Note]]"
    ---
    Some content
    Inline related notes: [[note1|alias1]] [[note2|alias2]]
    """
    note_properties = NoteProperties('', content)
    related_notes = note_properties.related_note
    expected_related_notes = {
        'yaml': {'title': ['Sample Note']},
        'inline': ['note1', 'note2']
    }
    assert related_notes == expected_related_notes
