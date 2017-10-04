django-lint
===========

Statically analyze Django projects for common problems.

## Checkers

### `field-verbose-name-capitalization`

Check that field verbose_names are not capitalized

### `model-explicit-str`

Check that all Models have __str__.

### `model-verbose-name-capitalization`

Check that model verbose_names are not capitalized

### `related-field-explicit-on-delete`

Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
an explicit `on_delete` clause.

### `related-field-explicit-related-name`

Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
an explicit `related_name`.

## Prior Art

* Lamby's [django-lint](https://github.com/lamby/django-lint)
