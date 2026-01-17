default: lint format_check lint_html html_format_check type_check test

lint:
    uv run ruff check

format_check:
    uv run ruff format --check

format:
    uv run ruff format

lint_html:
    uv run djlint cookie/templates/ --lint

html_format_check:
    uv run djlint cookie/templates/ --check

html_format:
    uv run djlint cookie/templates/ --reformat

type_check:
    uv run ty check

test:
    uv run pytest

squash:
    rm -f cookie/trails/migrations/0*.py
    rm -f db.sqlite3
    uv run python manage.py makemigrations trails
    uv run python manage.py migrate

runserver:
    uv run python manage.py runserver

families:
    uv run python manage.py loaddata data/families.json

super:
    uv run python manage.py createsuperuser