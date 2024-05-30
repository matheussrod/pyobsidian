
# Creating new search strategy

Sometimes, you will need to customize search strategies. `pyobsidian` provides a way to do that.

## The problem
Suppose, for some reason, you need to search for notes that filename contains a pattern. There is no such method by default. So, you need to create a new search strategy.

## Creating new strategy with default implementation
All strategies follow the same interface: [SearchBy](../reference/searchby.md). The following methods are defined in this interface:

- `search(notes: list[Note], field: Field)`
- `condition(note: Note, field: Field)`
- `__search(notes: list[Note], field: Field)`
- `is_valid_value(value: FieldValue)`
- `convert_field_value_to_list(value: FieldValue)`

However, a template with default implementation is provided (`SearchByDefault`). This class implements the methods in a way that they will generally be used. We can use it as a template to create new search strategies!

To do this, you will need to create a new class that inherits from `SearchByDefault` and implements `condition` method. For this hypothetical scenario, we would have:

```py
>>> from pyobsidian.searchby import SearchByDefault
>>> class SearchByFilenameRegex(SearchByDefault):
...     def condition(self, note: Note, field: Field) -> bool:
...         attr = getattr(note.properties, 'filename')
...         return any(re.findall(str(field.value), attr))
```

This simple code is enough to create a new search strategy. Now, you can add it to vault search strategies.

```py
>>> from pyobsidian.vault import Vault
>>> vault = Vault('your/obsidian/vault/path')
>>> vault.add_new_search_strategy(
...     'filename_regex', 
...     SearchByFilenameRegex
... )
>>> new_vault = (
...     vault
...     .find_by('filename_regex', 'test')
...     .execute()
... )
>>> notes_with_test_in_filename = new_vault.notes
```
