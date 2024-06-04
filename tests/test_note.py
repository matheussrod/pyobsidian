
from pyobsidian.note import Note

def test__eq__():
    note = Note('note/path', 'content')
    new_note = Note('note/path', 'content')
    assert note == new_note

def test__eq__different_object():
    note = Note('note/path', 'content')
    new_note = 'note'
    assert note != new_note

def test__hash__():
    note = Note('note/path', 'content')
    assert hash(note) == hash(note.path)

def test_propertie_properties():
    note = Note('note/path', 'content')
    assert note.properties

def test_note_read_file(tmp_path):
    tmp_file = tmp_path / 'test_read_file.md'
    content = 'content'
    tmp_file.write_text(content)
    note = Note(str(tmp_file))
    note_content = note.read()
    assert note_content == 'content'

def test_note_write_file(tmp_path):
    tmp_file = tmp_path / 'test_write_file.md'
    content = 'content'
    note = Note(str(tmp_file), content)
    note.write()
    file_content = tmp_file.read_text()
    assert content == file_content
