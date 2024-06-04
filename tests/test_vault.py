
from deepdiff import DeepDiff
from pyobsidian.adder import Adder, AdderField
from pyobsidian.adder_op import OpMkHeader
from pyobsidian.filter import Filter, FilterField, Field
from pyobsidian.formatter import Formatter
from pyobsidian.searchby import SearchBy
from pyobsidian.vault import Vault
import pytest

def test_vault_path():
    vault = Vault('some/path')
    assert vault.path == 'some/path'

def test_vault_empty_notes():
    vault = Vault('some/path')
    assert vault.notes == []

def test_vault_empty_filter():
    vault = Vault('some/path')
    assert vault.filter == Filter()

def test_vault_add_search_strategy():
    class NewStrategy(SearchBy):
        ...
    vault = Vault('some/path')
    vault.add_new_search_strategy('new', NewStrategy)
    assert vault.search_strategies['new'] == NewStrategy

def test_vault_add_new_adder_strategy():
    class NewAdderWhere:
        ...
    vault = Vault('some/path')
    vault.add_new_adder_strategy('new', NewAdderWhere)
    assert vault.adder_strategies['new'] == NewAdderWhere

def test_vault_add_new_formatter():
    class NewFormatter(Formatter):
        ...
    vault = Vault('some/path')
    vault.add_new_formatter('new', 'new', NewFormatter)
    assert vault.formatters[('new', 'new')] == NewFormatter

def test_vault_get_notes(vault_dir):
    vault = Vault(str(vault_dir))
    assert len(vault.get_notes()) == 3

def test_vault_find_by_immutability():
    vault = Vault('some/path')
    new_vault = vault.find_by('title', 'sample')
    assert vault != new_vault

def test_vault_find_by_new_filter():
    vault = Vault('some/path')
    filter_field = FilterField(
        Field('title', 'sample', 'file'),
        'and'
    )
    filter = Filter([filter_field])
    new_vault = vault.find_by('title', 'sample', 'file', 'and')
    assert new_vault.filter == filter

def test_vault_pipe_find_by_new_filters():
    vault = Vault('some/path')
    filter_field = FilterField(
        Field('title', 'sample', 'file'),
        'and'
    )
    filter = Filter([filter_field])
    new_vault = (
        vault
        .find_by('title', 'sample', 'file', 'and')
        .find_by('title', 'sample', 'file', 'and')
    )
    assert new_vault.filter == filter.add_field(filter_field)

def test_vault_execute_without_filter(vault_dir):
    vault = Vault(str(vault_dir))
    assert vault.execute() == vault

def test_vault_execute_without_adder(vault_dir):
    vault = Vault(str(vault_dir)).find_by('tag', 'tag1', 'file')
    new_vault = vault.execute()
    assert new_vault.filter == vault.filter \
        and new_vault.adder == vault.adder

def test_vault_execute_with_filter_and(vault_dir):
    vault = Vault(str(vault_dir))
    new_vault = (
        vault
        .find_by('tag', 'tag1')
        .execute()
    )
    assert len(new_vault.notes) == 3
    new_vault = (
        vault
        .find_by('tag', 'tag3')
        .execute()
    )
    assert len(new_vault.notes) == 1

def test_vault_execute_with_filter_or(vault_dir):
    vault = Vault(str(vault_dir))
    new_vault = (
        vault
        .find_by('tag', 'tag3')
        .execute()
    )
    assert len(new_vault.notes) == 1
    new_vault = (
        vault
        .find_by('tag', 'tag1', mode = 'or')
        .execute()
    )
    assert len(new_vault.notes) == 3

def test_vault_execute_raise_value_error_with_invalid_mode():
    vault = Vault('some/path')
    with pytest.raises(ValueError):
        vault.find_by('tag', 'tag1', mode = 'invalid').execute()

def test_vault_execute_raise_value_error_with_invalid_adder_where(vault_dir):
    vault = Vault(str(vault_dir)).find_by('tag', 'tag1', 'file')
    with pytest.raises(ValueError):
        vault.add('title', 'sample', 'invalid').execute()

def test_vault_execute_raise_value_error_with_invalid_adder_formatter(vault_dir):
    vault = Vault(str(vault_dir)).find_by('tag', 'tag1', 'file')
    with pytest.raises(ValueError):
        vault.add('invalid', 'sample', 'inline').execute()

def test_vault_execute_with_adder(vault_dir):
    vault = (
        Vault(str(vault_dir))
        .find_by('tag', 'tag3', 'inline')
        .execute()
    )
    note = vault.notes[0]
    content = note.properties.content
    vault.add('tag', 'sample', 'inline').execute()
    with open(note.path, 'r', encoding='utf8') as file:
        new_content = file.read()
    assert new_content != content

def test_vault_add_immutability():
    vault = Vault('some/path')
    new_vault = vault.add('title', 'sample', 'file')
    assert vault != new_vault

def test_vault_add_new_adder():
    vault = Vault('some/path')
    adder_field = AdderField('title', 'sample', 'file')
    adder = Adder([adder_field])
    new_vault = vault.add('title', 'sample', 'file')
    assert new_vault.adder == adder

def test_vault_pipe_add_new_adders():
    vault = Vault('some/path')
    adder_field = AdderField('title', 'sample', 'file')
    adder = Adder([adder_field])
    new_vault = (
        vault
        .add('title', 'sample', 'file')
        .add('title', 'sample', 'file')
    )
    assert new_vault.adder == adder.add_field(adder_field)

def test_vault_add_new_adder_with_op():
    vault = Vault('some/path')
    adder_field = AdderField('title', 'sample', ('mkheader', OpMkHeader('|>{1}h1')))
    adder = Adder([adder_field])
    new_vault = vault.add('title', 'sample', OpMkHeader('|>{1}h1'))
    assert DeepDiff(new_vault.adder, adder, ignore_order=True) == {}
