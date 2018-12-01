# 0.4.3

### Bugfixes

* Fix link to poyo on PyPI, thanks to
  [@mrshu][@mrshu] (#20)

[@mrshu]: https://github.com/mrshu

# 0.4.2

### Bugfixes

* Resolve a bug with list items and comments, thanks to
  [@ishanarora][@ishanarora] (#18)

[@ishanarora]: https://github.com/ishanarora

# 0.4.1

### Bugfixes

* Update regex patterns to allow for no newline at the end of the given string,
  thanks to [@mikeckennedy][@mikeckennedy] and [@hackebrot][@hackebrot]
  (#13, #14)

[@mikeckennedy]: https://github.com/mikeckennedy

# 0.4.0

### Features

* Add support for block comments in sections, thanks to [@jakubka][@jakubka]
  and [@hackebrot][@hackebrot] (#7)

```yaml
default_context: # foobar
    greeting: こんにちは
    # comment
    # allthethings
    docs: true

    123: 456.789
```

### Improvements

* Set up ``poyo`` logger with NullHandler to log DEBUG messages when parsing,
  thanks to [@hackebrot][@hackebrot]

```text
DEBUG:poyo.parser:parse_simple <-     123: 456.789
DEBUG:poyo.parser:parse_int <- 123
DEBUG:poyo.parser:parse_int -> 123
DEBUG:poyo.parser:parse_float <- 456.789
DEBUG:poyo.parser:parse_float -> 456.789
DEBUG:poyo.parser:parse_simple -> <Simple name: 123, value: 456.789>
```

### Bugfixes

* Fix an issue around section names if the line contained more than one colon
  symbol, thanks to [@gvalkov][@gvalkov] and [@hackebrot][@hackebrot] (#9)
* Fix an issue that caused partial matches to raise an error, thanks to
  [@gvalkov][@gvalkov] and [@hackebrot][@hackebrot] (#9)

[@gvalkov]: https://github.com/gvalkov
[@hackebrot]: https://github.com/hackebrot
[@jakubka]: https://github.com/jakubka


# 0.3.0

### Features

* Add support for blank lines and comment lines in lists, thanks to
  [@eykd][@eykd] and [@hackebrot][@hackebrot] (#5)

```yaml
doc_tools:
    # docs or didn't happen
    -    mkdocs
    - 'sphinx'

    - null
```

### Improvements

* Add tests for patterns, thanks to [@eykd][@eykd] and [@hackebrot][@hackebrot]
  (#5)

### Bugfixes

* Solve an issue with ``~`` character not being recognized as ``None``

[@eykd]: https://github.com/eykd
[@hackebrot]: https://github.com/hackebrot


# 0.2.0

### Features

* Add support for list values

```yaml
doc_tools:
    - mkdocs
    - 'sphinx'
    - null
```
* Expose ``PoyoException`` in API

```python
from poyo import PoyoException
```

### Bugfixes

* Ignore dashes in lines

```yaml
---
default_context:
    foo: "hallo #welt" #Inline comment :)
    docs: true
```


# 0.1.0

First release on PyPI.

### Features

* ``parse_string()`` to load a YAML string as a Python dict
