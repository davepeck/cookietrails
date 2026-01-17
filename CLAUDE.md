# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands use `uv` and are defined in `justfile`:

- `just` - Run full CI pipeline (lint, format check, type check, test)
- `just lint` - Python linting with ruff
- `just format` - Auto-format Python code
- `just lint_html` - Lint Django templates with djlint
- `just html_format` - Auto-format Django templates
- `just type_check` - Type checking with ty
- `just test` - Run Django tests
- `just runserver` - Start development server
- `just squash` - Reset migrations and database (dev only)

## Architecture

CookieTrails is a Django 6.x app for tracking Girl Scout cookie inventory across multiple physical locations.

**Core concept:** Tracks three event types for cookies assigned to the troop but held by families:
- Distributions (troop → family)
- Returns (family → troop)
- Counts (physical inventory by family)

**Stack:**
- Django 6.x with PostgreSQL (prod) / SQLite (dev)
- HTMX for frontend interactivity
- Tailwind CSS via CDN

**Structure:**
- `cookie/` - Django project package
- `cookie/trails/` - Main app with models, views, admin
- `cookie/templates/` - Django templates (djlint formatted, 2-space indent)

## Family Authentication

Families authenticate via email address only (no password). This is intentionally simple since families already have their email on file with Girl Scouts.

**How it works:**
- Family enters their email at `/family/login/`
- If email matches a `Family` record, they're logged in (stored in session)
- If not found, they see an error and can retry
- This is completely separate from Django's User/admin authentication

**Key files:**
- `cookie/trails/family_auth.py` - Session helpers and `@requires_family` decorator
- `cookie/trails/context_processors.py` - Adds `current_family` to all templates

**Usage:**
- Use `@requires_family` decorator (or `@method_decorator(requires_family, name="dispatch")` for CBVs) on views that need a family
- Access `current_family` in templates (will be `None` if not logged in)
- Decorator redirects to `/family/login/?next=...` if no family in session
