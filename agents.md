# Agents Guide

This file is the first stop for any AI or automation working in this repository.
It should reduce the need to scan the whole project before making a change.

## Project Summary

Streamlit dashboard for sales and invoice tracking, with authentication, role-based access, CSV import, and Supabase persistence.

## Active Entry Point

- `main.py` is the current app entry point.
- `app.py` may exist as legacy or alternate wiring, but `main.py` is the preferred place to inspect first.

## Core Areas

- `src/auth/`
  - Session login, logout, and current-user helpers.
  - Role data is stored in Streamlit session state.
- `src/dashboard/`
  - Page setup, global styles, and reusable UI components.
  - `config.py` controls page chrome and must not hide the sidebar collapse control.
- `src/data/`
  - Data loading, CSV preprocessing, schema validation, and Supabase access.
  - The dashboard should use live database data, not mocks.

## Main Data Flow

- Login happens first.
- `main.py` loads the current user and decides which UI sections are visible.
- Dashboard data comes from `src/data/loader.py` and Supabase-backed helpers.
- CSV imports go through `src/data/uploader.py` and are written with the Supabase client layer.

## Working Rules

- Prefer small, local changes that match the existing structure.
- Do not reintroduce mock data when a live data path exists.
- Preserve admin-only behavior for upload actions.
- Keep the sidebar collapse button visible.
- Prefer `uv run ...` for commands, tests, and scripts.

## Before Editing

- Check the current entry point and the nearest owning module.
- Confirm whether the change belongs to auth, dashboard, or data.
- Use the smallest relevant code path instead of broad search.

## Update Policy

- This file must be updated whenever the project architecture, data flow, commands, or user-facing behavior changes.
- If a change affects any module, flow, or assumption documented here, update this file in the same work.
- Keep it current so future AI agents can rely on it without reading every file.

## Useful Commands

- `uv run streamlit run main.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format .`
