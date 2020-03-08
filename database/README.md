# Portfolio Compiler

## Renders directory structure

```
renders/
  <collection name>/
    description.md
    <product name>/
      description.md
      variants.toml
```

## Collection
Include a front matter in `description.md` with the following properties:

| property | description | default |
|----------|-------------|---------|
| id       | A unique indentifier | The parent folder's name|
| name     | The name used in the interface | The id, title-cased.
| website  | A link to the client's website | `""`
| tags     | A list of tags. | `[]`

## Product
Include a front matter in `description.md` with the following properties:

| property | description | default |
|----------|-------------|---------|
| id       | A unique indentifier | The parent folder's name|
| name     | The name used in the interface | The id, title-cased.
| website  | A link to the client's website | `""`
| tags     | A list of tags. | The collection's tags

## Variants

```toml
[wide]
```
