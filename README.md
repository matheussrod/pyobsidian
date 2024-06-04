# pyobsidian

## Overview

`pyobsidian` is a python library for working with Obsidian vaults. It's allows you to find and manipulate any note in your Obsidian vault.

## Installation
```python
pip install pyobsidian
```

## Usage

A common workflow used in this library is to define a vault, create a sequence of steps, and execute it to manipulate notes. This workflow can be seen below. This workflow can see bellow:

<p style="text-align: center;">
    <img src="https://raw.githubusercontent.com/matheussrod/pyobsidian/main/docs/assets/imgs/workflow.svg">
</p>

This can be translated to code in a very simple way.
```python
>>> from pyobsidian.vault import Vault
>>> from pyobsidian.adder_op import OpMkHeader
>>> vault = Vault('your/obsidian/vault/path')
>>> new_vault = (
...    vault
...    .find_by('folder', 'some_folder')
...    .find_by('tag', 'some_tag')
...    .add('content', '# Some header', OpMkHeader('|>{1}h1'))
...    .execute()
...)
>>> print(vault)
Vault(
    path='your/obsidian/vault/path',
    notes=[],
    filter=Filter(),
    adder=Adder()
)
>>> print(new_vault)
Vault(
    path='your/obsidian/vault/path',
    notes=[Note(path='your/obsidian/vault/path/.../note.md')],
    filter=Filter(
        [
            FilterField(Field(key='folder', value='some_folder', occurrence='file'), mode = 'and'),
            FilterField(Field(key='tag', value='some_tag', occurrence='file'), mode = 'and')
        ]
    ),
    adder=Adder(
        [
            AdderField(key='content', value='# Some header', where=OpMkHeader('<|{1}h1'))
        ]
    )
)
>>> print(new_vault.notes)
[Note(path='your/obsidian/vault/path/.../note.md')]
```

## Getting help
If you encounter a clear bug, please file an issue with a minimal reproducible example on GitHub.
