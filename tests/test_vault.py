
from pyobsidian.vault import Vault
from pyobsidian.filter import Filter, FilterField, Field
from pyobsidian.searchby import SearchBy
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

def test_vault_execute_with_filter(vault_dir):
    vault = Vault(str(vault_dir))
    new_vault = (
        vault
        .find_by('tag', 'tag1', 'file')
        .execute()
    )
    assert len(new_vault.notes) == 3

def test_vault_execute_with_filter_inline(vault_dir):
    vault = Vault(str(vault_dir))
    new_vault = (
        vault
        .find_by('tag', 'tag3', 'file')
        .execute()
    )
    assert len(new_vault.notes) == 1

def test_vault_execute_with_filter_yaml(vault_dir):
    vault = Vault(str(vault_dir))
    new_vault = (
        vault
        .find_by('tag', 'tag', 'yaml')
        .execute()
    )
    assert len(new_vault.notes) == 1

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
