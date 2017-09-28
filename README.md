django-lint
===========

Statically analyze Django projects for common problems.

## Checkers

### `model-explicit-str`
Check that all Models have __str__.
### `related-field-explicit-on-delete`

Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
an explicit `on_delete` clause.

### `related-field-explicit-related-name`

Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
an explicit `related_name`.

## Prior Art

* Lamby's [django-lint](https://github.com/lamby/django-lint)
