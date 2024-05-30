
from pyobsidian.note import Note

def test__eq__(note_reader):
    note = Note(note_reader.path)
    new_note = Note(note_reader.path)
    assert note == new_note

def test__eq__different_object(note_reader):
    note = Note(note_reader.path)
    new_note = 'note'
    assert note != new_note

def test__hash__(note_reader):
    note = Note(note_reader.path)
    assert hash(note) == hash(note.path)

def test_propertie_properties(note_reader):
    note = Note(note_reader.path)
    assert note.properties
