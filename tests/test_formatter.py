
from pyobsidian.formatter import *

# Inlines --------------------------------------------------------------------
## Tags ----------------------------------------------------------------------
def test_formatter_tag_inline_one_str():
    formatter = FormatterTagInline()
    assert formatter.format('content') == '\n\n#content\n\n'

def test_formatter_tag_inline_one_str_formated_as_tag():
    formatter = FormatterTagInline()
    assert formatter.format('#content') == '\n\n#content\n\n'

def test_formatter_tag_inline_multiple_list():
    formatter = FormatterTagInline()
    assert formatter.format(['content1', 'content2']) == '\n\n#content1 #content2\n\n'

def test_formatter_tag_inline_multiple_list_formated_as_tag():
    formatter = FormatterTagInline()
    assert formatter.format(['content1', '#content2']) == '\n\n#content1 #content2\n\n'

## Related Notes -------------------------------------------------------------
def test_formatter_related_note_inline_one_str():
    formatter = FormatterRelatedNoteInline()
    assert formatter.format('content') == '\n\n- [[content]]\n\n'

def test_formatter_related_note_inline_one_str_formated_as_related_note():
    formatter = FormatterRelatedNoteInline()
    assert formatter.format('[[content]]') == '\n\n- [[content]]\n\n'

def test_formatter_related_note_inline_list():
    formatter = FormatterRelatedNoteInline()
    assert formatter.format(['content1', 'content2']) == '\n\n- [[content1]]\n- [[content2]]\n\n'

def test_formatter_related_note_inline_list_formated_as_related_note():
    formatter = FormatterRelatedNoteInline()
    assert formatter.format(['content1', '[[content2]]']) == '\n\n- [[content1]]\n- [[content2]]\n\n'

## Content -------------------------------------------------------------------
def test_formatter_content_inline_one_str():
    formatter = FormatterContentInline()
    assert formatter.format('content') == '\n\ncontent\n\n'

def test_formatter_content_inline_list():
    formatter = FormatterContentInline()
    assert formatter.format(['content1', 'content2']) == '\n\ncontent1\n\ncontent2\n\n'

# Yamls ----------------------------------------------------------------------
## Related Notes -------------------------------------------------------------
def test_formatter_related_note_yaml():
    formatter = FormatterRelatedNoteYaml()
    assert formatter.format(['content']) == ['[[content]]']
