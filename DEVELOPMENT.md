# Development

## TODO
- Add support to `Last-Modified` HTTP header when using cache.
- Check if domains are still active.
- Improve source lists encoding support (namely, allow compressed files).

## Tests
```bash
poetry install
poetry run coverage run -m pytest
poetry run coverage report -m
```

## Linting
```bash
poetry run ruff check hostblocker/ tests/
poetry run mypy hostblocker/ tests/
```
