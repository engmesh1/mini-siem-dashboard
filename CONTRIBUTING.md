# Contributing

Thanks for contributing!

## Dev setup
- Python 3.10+
- Create venv and install dependencies:
  ```bash
  cd backend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## Lint
```bash
cd backend
ruff check .
```

## Tests
```bash
cd backend
pytest -q
```

## Commit style
- Keep commits small and focused.
- Prefer descriptive messages: `feat: add csv export endpoint`
