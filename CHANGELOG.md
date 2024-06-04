# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-06-04
### Added
- Helpers functions
- Utilities for working with markdown to enable parsing and obtaining headers
- `AdderWhere` to enable additions in specific locations of notes
- `Op` to enable extensions in content additions, allowing users to define new forms of addition
- `Formatter` for formatting the content to be added
- `Adder` provisioned by `add` in `Vault`, allowing you to add content to filtered notes
- methods `read` and `write` in `Note` class

### Removed
- `NoterReader` was removed, passing method to` Note`

## [0.1.1] - 2024-05-30

### Removed
- Development packages from the build

## [0.1.0] - 2024-05-30

### Added
- `Note` class to represent a note in Obsidian vault
- `Filter` class to represent an filter
- `SearchBy` class to represent search strategy
- `Vault` class to represent an Obsidian vault
