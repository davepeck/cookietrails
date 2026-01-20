# Repository Guidelines

## Project Structure & Module Organization
- `cookie/` is the Django project package.
- `cookie/trails/` is the primary app (models, views, admin, templates).
- `cookie/templates/` holds Django templates (formatted via djlint).
- `data/` contains fixtures (e.g., `data/families.json`).
- `manage.py` is the Django entrypoint; `db.sqlite3` is the local dev database.

## Build, Test, and Development Commands
Use `just` (backed by `uv`) for common workflows:
- `just` runs the full CI-style pipeline (lint, format check, type check, tests).
- `just runserver` starts the local Django server.
- `just test` runs pytest with the configured Django settings.
- `just lint` / `just format` run ruff checks or auto-format.
- `just lint_html` / `just html_format` check or reformat templates with djlint.
- `just squash` resets dev migrations and `db.sqlite3` (local dev only).
- `just families` loads the `data/families.json` fixture.

## Coding Style & Naming Conventions
- Python follows ruff defaults; auto-format with `just format`.
- Django templates use 2-space indentation (`djlint` profile).
- Tests live under `cookie/` and are named `*_tests.py` or `tests.py`.
- Prefer clear, domain-specific names (e.g., `Distribution`, `Return`, `Count`).

## Testing Guidelines
- Frameworks: `pytest` + `pytest-django`.
- Settings: `DJANGO_SETTINGS_MODULE=cookie.settings` (handled by pytest config).
- Run all tests: `just test`. Keep new tests close to the app being changed.

## Commit & Pull Request Guidelines
- Commit messages are short, imperative, and specific (e.g., "Add indexes").
- PRs should explain the motivation, list key changes, and include UI screenshots
  when templates or HTMX interactions change.

## Configuration Tips
- The app targets Django 6.x and Python 3.14+.
- Production commonly uses Postgres; local dev uses SQLite by default.
