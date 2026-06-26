# Agents Guide

This file is the first stop for any AI or automation working in this repository.
It should reduce the need to scan the whole project before making a change.

---

# Project Summary

Streamlit dashboard for sales and invoice tracking, with authentication, role-based access, CSV import, and Supabase persistence.

---

# Active Entry Point

- `main.py` is the current app entry point.
- `main.py` is the preferred place to inspect first.

---

# Core Areas

## `src/auth/`

- Session login, logout, and current-user helpers.
- Role data is stored in Streamlit session state.

## `src/dashboard/`

- Page setup.
- Global styles.
- Reusable UI components.
- Theme configuration.
- KPI cards.
- Tables.
- Charts.
- Filters.

`config.py` controls page chrome and **must not hide the sidebar collapse control.**

## `src/data/`

- Data loading.
- CSV preprocessing.
- Schema validation.
- Supabase access.

The dashboard must always use live database data instead of mocks.

---

# Main Data Flow

1. User authentication.
2. Current user is loaded.
3. Role determines available actions.
4. Data is fetched from Supabase.
5. Sidebar filters are applied.
6. KPIs are calculated.
7. Tables and charts are rendered.
8. Export buttons generate PDF or Excel using filtered data.

---

# Dashboard Layout

The application should follow a clean business intelligence layout inspired by Microsoft Power BI.

Recommended page hierarchy:

- Header
    - Title
    - Export buttons
    - User information

- KPI Row
    - Summary cards
    - Equal spacing
    - Responsive layout

- Main Content
    Left:
    - Detailed tables
    - Transaction history

    Right:
    - Charts
    - Distribution insights
    - Rankings

- Sidebar
    - Global filters
    - Collapsible
    - Fixed position

---

# Design Guidelines

The dashboard should prioritize readability, density of information and professional appearance.

## Visual Style

Preferred style:

- Modern
- Flat Design
- Enterprise dashboard
- Similar to Power BI
- Minimalistic
- High information density
- Clean spacing

Avoid:

- Gradients
- Glassmorphism
- Excessive shadows
- Neon colors
- Rounded elements larger than necessary
- Decorative animations

---

# Color Palette

Keep the current company identity.

Primary color:

Dark Green

Suggested palette:

Primary
- #0F5A38

Primary Hover
- #136B43

Dark
- #083C28

Success
- #4CAF50

Warning
- #FFC107

Danger
- #D9534F

Background
- #F5F6F8

Cards
- #FFFFFF

Borders
- #E5E7EB

Primary Text
- #202124

Secondary Text
- #5F6368

Charts should always use solid colors.

Do not use gradients in:

- charts
- buttons
- cards
- backgrounds

---

# Components

## KPI Cards

Should contain:

- Icon
- Label
- Main value
- Optional secondary information

Characteristics:

- White background
- Solid green icon
- Thin border
- Small radius
- Consistent height
- Equal spacing

---

## Tables

Preferred characteristics:

- Sticky header
- Zebra rows
- Compact spacing
- Hover highlight
- Sortable columns
- Pagination when necessary

Avoid excessive row height.

---

## Sidebar

Filters should be organized in logical order.

Suggested order:

- Client
- City
- State
- Product Code
- Product Description
- Sales Order
- Invoice Date

Each filter should:

- occupy full width
- have consistent spacing
- update the dashboard immediately

---

# Charts

Charts should prioritize readability over visual effects.

Recommended:

- Bar Chart
- Horizontal Bar Chart
- Line Chart
- Area Chart
- Donut Chart
- Treemap (when appropriate)

Avoid:

- 3D charts
- Pie charts with many categories
- Heavy shadows
- Gradient fills

All charts should:

- Use solid colors
- Display labels when appropriate
- Include legends only when necessary
- Maintain consistent spacing

---

# Typography

Prefer clean sans-serif fonts.

Hierarchy:

Title
- Bold

Section Title
- SemiBold

Card Value
- Large
- Bold

Labels
- Medium

Table
- Compact

---

# Responsiveness

The dashboard should adapt to:

- Desktop
- Laptop
- Tablet

KPI cards should wrap automatically.

Charts should resize without clipping.

Tables should maintain horizontal scrolling when necessary.

---

# Functional Requirements

The dashboard should support:

- Multi-filtering
- Cross-filtering
- Export to PDF
- Export to Excel
- Fast rendering
- Live data updates
- Role-based visibility

Admin users:

- CSV upload
- Data management

Regular users:

- View
- Filter
- Export

---

# Working Rules

- Prefer small, local changes.
- Preserve existing architecture.
- Never replace live data with mock data.
- Preserve admin-only functionality.
- Keep sidebar collapse control visible.
- Maintain visual consistency across all pages.
- Follow the design guidelines above when introducing new UI components.

---

# Before Editing

- Inspect `main.py`.
- Identify the owning module.
- Make the smallest possible change.
- Respect the established visual language.
- Reuse existing components whenever possible.

---

# Update Policy

Update this document whenever:

- Architecture changes.
- Data flow changes.
- New modules are introduced.
- Dashboard layout changes.
- Design system changes.
- New global components are added.

---

# Useful Commands

```bash
uv run streamlit run main.py
uv run pytest
uv run ruff check .
uv run ruff format .
```

---

# Logging & Debug

This project now includes a lightweight application logging system to help
validate CSV uploads, data loads and backend operations. Key points:

- Log file: `logs/app.log` (rotating handler, up to ~5MB per file, 3 backups).
- Levels: use INFO for normal events and ERROR/EXCEPTION for failures.
- Front-end: the Streamlit UI exposes recent logs to admins via the
  "Logs recentes (backend)" expander (component: `src/dashboard/components/logs.py`).

When troubleshooting, check:

1. The Streamlit logs expander after reproducing the issue in the UI.
2. The `logs/app.log` file on the server for full context and stack traces.

When writing code, prefer `from src.logging import setup_logger` and create a
module logger with `logger = setup_logger(__name__)` and call `logger.info(...)`
or `logger.exception(...)` on errors.
