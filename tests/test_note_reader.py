
def test_read_file(note_reader, content):
    note_content = note_reader.read()
    assert note_content == content
