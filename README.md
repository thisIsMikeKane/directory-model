# Directory Model
`directory_model` is a Python package for both modeling and validating filesystem directory structures based on YAML schema definitions. It provides a class-based model for referencing paths, built on Python's Path package and Pydantic.

## Installation

```bash
pip install directory_model
```

## `directory.yml`

The `directory.yml` file contains the schema that the contents of your directory will be validated against. The `directory.yml` should contain a top level `path:` and may contain a top level `config:`.

`path:`

`config:`
