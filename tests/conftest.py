
from pyobsidian.filter import Field, FilterField
from pyobsidian.note import Note, NoteReader
import pytest
import shutil
import tempfile
import os

@pytest.fixture(scope='session')
def content():
    content = """       
    ---
    title: Sample Note
    tags: [test, sample]
    date: "{{date}}"
    ---
    This is a sample note for testing purposes.
    Inline tags: #tag1 #tag2
    """
    return content

@pytest.fixture(scope='session')
def content2():
    content = """       
    ---
    title: Sample Note
    tags: [test, sample, tag]
    date: "{{date}}"
    ---
    This is a sample note for testing purposes.
    Inline tags: #tag1 #tag2 #tag3
    """
    return content

@pytest.fixture()
def invalid_yaml_content():
    invalid_content = """       
    ---
    any: {{"invalid"}}
    ---
    """
    return invalid_content

@pytest.fixture()
def note_reader(tmp_path, content):
    tmp_file = tmp_path / 'test_file.md'
    tmp_file.write_text(content)
    note_reader = NoteReader(str(tmp_file))
    return note_reader

@pytest.fixture()
def note(note_reader):
    return Note(note_reader.path)

@pytest.fixture()
def field():
    return Field('content', 'value', 'file')

@pytest.fixture()
def filter_field():
    return FilterField(Field('folder', 'value', 'file'), 'and')

@pytest.fixture(scope='session')
def vault_dir(content, content2):
    tmp_dir = tempfile.mkdtemp()
    subfolder = os.path.join(tmp_dir, 'folder')
    os.makedirs(subfolder)

    files_content = {
        'note.md': content,
        os.path.join('folder', 'note2.md'): content,
        'note3.md': content2,
        'file.txt': 'txt file'
    }
    for filename, content in files_content.items():
        with open(os.path.join(tmp_dir, filename), 'w') as f:
            f.write(content)

    yield tmp_dir
    shutil.rmtree(tmp_dir)
