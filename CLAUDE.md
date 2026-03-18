# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Sistema Alba is a desktop ERP application for Brazilian businesses, built with Python + Tkinter/ttkbootstrap using an MDI (Multiple Document Interface) pattern. The UI intentionally mimics a classic Windows XP aesthetic.

## Running the Application

**macOS (requires Homebrew Tk):**
```bash
brew install tcl-tk python-tk@3.13
/opt/homebrew/bin/python3.13 -m venv .venv-macos
./.venv-macos/bin/python -m pip install -r requirements.txt
./run-macos.sh
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Building

```bash
# Windows executable (CX_Freeze)
python setup.py build
# Output: dist/alba
```

## Testing

```bash
python test_contatos.py
```

There is no full test suite — `test_contatos.py` is the only test file and covers the contacts module.

## Architecture

### Startup Flow

```
main.py → App(ttkb.Window)
           ├─ _configure_macos_locale()
           ├─ aplicar_estilo()  ← estilo.py
           ├─ MDIContainer()    ← mdi.py
           └─ create_menus()   → opens windows/ on click
```

### Window Hierarchy

```
MDIChild (mdi.py)
  └─ BaseWindow (windows/base_window.py)
       └─ Every feature window (windows/*.py)
```

`BaseWindow` provides: database connectivity (`self.conectar()`), recnum generation (`self.get_next_recnum(table)`), message display (`self.show_message()`), two-step delete confirmation, and record navigation.

### Database

- SQLite at `database/alba.db` (overridable via `ALBA_DB_PATH` env var)
- Every table uses a `recnum` sequential integer as primary identifier
- Inserts use `BEGIN IMMEDIATE` transactions with up to 3 retries + exponential backoff
- The text factory handles both UTF-8 and latin1 to accommodate legacy data
- Recnum operations are logged to `alba_recnum.log`

### Adding a New Window

Each window in `windows/` follows this pattern:

1. Subclass `BaseWindow`
2. Constructor calls `aplicar_estilo()`, sets `self.current_id` / `self.current_recnum`
3. Build a toolbar with emoji buttons (➕💾🗑️⏮◀▶⏭) and a blue message panel
4. Implement: `novo()`, `salvar()`, `remover()`, `carregar_*()`, `on_select()`
5. Register the window in `main.py`'s `create_menus()` method

### Styling

`estilo.py` defines all colors, fonts, and widget styles. The palette is:
- Background: `#d4d0c8` (light gray)
- Entries: `#ffffff`
- Selection: `#0a246a` (dark blue)
- Messages: blue=info, green=success, orange=warning, red=error

Messages auto-clear after 5 seconds for info/success; errors persist until dismissed.

## Key Conventions

- **Brazilian Portuguese** is used throughout: labels, messages, variable names, and comments.
- Toolbar buttons use emoji icons, not image assets.
- All database writes go through `BaseWindow` helpers — avoid raw `sqlite3` calls in window classes.
- `recnum` is not the same as SQLite `rowid`; never assume they match.
