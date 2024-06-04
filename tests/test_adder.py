
from pyobsidian.note import Note
from pyobsidian.adder import *
from pyobsidian.adder_op import OpMkHeader
import pytest

# AdderWhereInline -----------------------------------------------------------
def test_adder_where_inline_when_note_has_yaml():
    content = '---\nkey: value\n---\ncontent'
    note = Note('note/path', content)
    adder = AdderWhereInline()
    adder_field = AdderField('key', 'value', 'inline')
    adder_exec = adder.exec(note, adder_field)
    expected = '---\nkey: value\n---\nvaluecontent'
    assert  adder_exec == expected

def test_adder_where_inline_when_note_has_not_yaml():
    note = Note('note/path', '')
    adder = AdderWhereInline()
    adder_field = AdderField('key', 'value', 'inline')
    adder_exec = adder.exec(note, adder_field)
    expected = 'value'
    assert  adder_exec == expected

# AdderWhereYaml -------------------------------------------------------------
def test_adder_where_yaml_when_note_has_yaml():
    content = '---\nkey: value\n---\ncontent'
    note = Note('note/path', content)
    adder = AdderWhereYaml()
    adder_field = AdderField('key2', 'value2', 'yaml')
    adder_exec = adder.exec(note, adder_field)
    expected = '---\nkey: value\nkey2:\n- value2\n---\ncontent'
    assert  adder_exec == expected

def test_adder_where_yaml_when_note_has_not_yaml():
    note = Note('note/path', '')
    adder = AdderWhereYaml()
    adder_field = AdderField('key', 'value', 'yaml')
    adder_exec = adder.exec(note, adder_field)
    expected = '---\nkey:\n- value\n---\n\n'
    assert  adder_exec == expected

def test_adder_where_yaml_when_value_is_duplicate():
    content = '---\nkey: value\n---\ncontent'
    note = Note('note/path', content)
    adder = AdderWhereYaml()
    adder_field = AdderField('key', 'value', 'yaml')
    adder_exec = adder.exec(note, adder_field)
    new_note = Note('note/path', adder_exec)
    yaml = new_note.properties.yaml_content['key']
    assert yaml == ['value']

def test_adder_where_yaml_when_key_is_duplicate():
    content = '---\nkey: value\n---\ncontent'
    note = Note('note/path', content)
    adder = AdderWhereYaml()
    adder_field = AdderField('key', 'value2', 'yaml')
    adder_exec = adder.exec(note, adder_field)
    new_note = Note('note/path', adder_exec)
    yaml = new_note.properties.yaml_content['key']
    assert set(yaml) == set(['value', 'value2'])

def test_adder_where_yaml_when_key_is_list():
    content = '---\nkey:\n- value\n---\ncontent'
    note = Note('note/path', content)
    adder = AdderWhereYaml()
    adder_field = AdderField('key', 'value2', 'yaml')
    adder_exec = adder.exec(note, adder_field)
    new_note = Note('note/path', adder_exec)
    yaml = new_note.properties.yaml_content['key']
    assert set(yaml) == set(['value', 'value2'])

# AdderWhereOpMkHeader -------------------------------------------------------
def test_adder_where_op_mk_header_raise_error_when_where_is_not_tuple():
    note = Note('note/path', '')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', 'mkheader')
    with pytest.raises(ValueError):
        adder.exec(note, adder_field)

def test_adder_where_op_mk_header_raise_error_when_op_is_not_valid():
    note = Note('note/path', '')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', ('mkheader', 'invalid'))
    with pytest.raises(ValueError):
        adder.exec(note, adder_field)

def test_adder_where_op_mk_header_note_without_headers():
    note = Note('note/path', '')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', ('mkheader', OpMkHeader('|>{1}h1')))
    adder_exec = adder.exec(note, adder_field)
    assert adder_exec is None

def test_adder_where_op_mk_header_note_with_header_not_matching_op():
    note = Note('note/path', '# H1')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', ('mkheader', OpMkHeader('|>{2}h1')))
    adder_exec = adder.exec(note, adder_field)
    assert adder_exec is None

def test_adder_where_op_mk_header_note_with_header_matching_op_forward():
    note = Note('note/path', '# H1')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', ('mkheader', OpMkHeader('|>{1}h1')))
    adder_exec = adder.exec(note, adder_field)
    assert adder_exec == '# H1value'

def test_adder_where_op_mk_header_note_with_header_matching_op_backward():
    note = Note('note/path', '# H1')
    adder = AdderWhereOpMkHeader()
    adder_field = AdderField('key', 'value', ('mkheader', OpMkHeader('<|{1}h1')))
    adder_exec = adder.exec(note, adder_field)
    print(adder_exec)
    assert adder_exec == 'value# H1'

# AdderRegistry ---------------------------------------------------------------
def test_adder_registry_get_where_with_existing_key():
    adder_registry = AdderRegistry()
    assert adder_registry.get_where('inline')

def test_adder_registry_get_where_with_non_existing_key():
    adder_registry = AdderRegistry()
    assert adder_registry.get_where('non_existing_key') is None

def test_adder_registry_add_registry():
    class NewRegistry(AdderRegistry):
        ...
    adder_registry = AdderRegistry()
    adder_registry.add_registry('new', NewRegistry)
    assert adder_registry.get_where('new') == NewRegistry

def test_adder_registry_get_formatter_with_existing_key():
    adder_registry = AdderRegistry()
    assert adder_registry.get_formatter('tag', 'inline')

def test_adder_registry_get_formatter_with_non_existing_key():
    adder_registry = AdderRegistry()
    assert adder_registry.get_formatter('non_existing_key', 'inline') is None

def test_adder_registry_get_formatter_with_tuple():
    adder_registry = AdderRegistry()
    assert adder_registry.get_formatter('tag', ('mkheader', OpMkHeader('|>{1}h1')))

def test_adder_registry_add_formatter():
    class NewFormatter(Formatter):
        ...
    adder_registry = AdderRegistry()
    adder_registry.add_formatter('new', 'inline', NewFormatter)
    assert adder_registry.get_formatter('new', 'inline') == NewFormatter

# Adder -----------------------------------------------------------------------
def test_adder_add_field():
    adder = Adder()
    adder_field = AdderField('key', 'value', 'inline')
    new_adder = adder.add_field(adder_field)
    assert new_adder.fields == [adder_field]

def test_adder__eq__():
    adder1 = Adder()
    adder2 = Adder()
    assert adder1 == adder2

def test_adder__eq__with_different_fields():
    adder1 = Adder()
    adder2 = Adder().add_field(AdderField('key', 'value', 'inline'))
    assert not adder1 == adder2

def test_adder__eq__with_different_objects():
    adder1 = Adder()
    adder2 = any
    assert not adder1 == adder2
