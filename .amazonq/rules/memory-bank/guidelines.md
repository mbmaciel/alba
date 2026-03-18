# Alba System - Development Guidelines

## Code Quality Standards

### Import Organization
- **Standard Pattern**: Import ttkbootstrap first, then tkinter, followed by project modules
- **Consistent Structure**: `import ttkbootstrap as ttkb`, `from ttkbootstrap.constants import *`, `import tkinter as tk`
- **Project Imports**: Always import `estilo` and `BaseWindow` after standard libraries
- **Database Import**: `import sqlite3` for database operations

### Class Structure and Inheritance
- **Base Class Pattern**: All window classes inherit from `BaseWindow`
- **Constructor Pattern**: Always call `super().__init__(master)` first
- **Initialization Sequence**: Apply styling, set title, configure size, then build UI
- **State Management**: Initialize `current_id` and `current_recnum` attributes for record tracking

### Window Configuration Standards
- **Title Format**: Use descriptive titles with table references (e.g., "Cadastro de Pessoas (alba0001)")
- **Size Standards**: Common sizes are 900x600, 1100x700, 1200x800 based on complexity
- **Padding**: Use consistent padding of 10 pixels for main frames

## UI Framework Patterns

### Layout Architecture
- **Frame Hierarchy**: Main frame → Top frame (toolbar + messages) → Input frame → Tree frame
- **Toolbar Pattern**: Raised border with padding=5, contains button containers and separators
- **Message Panel**: Standardized message display with title and colored text
- **Input Layout**: Grid-based layout with consistent spacing and alignment

### Widget Standards
- **Button Icons**: Use Unicode symbols (➕ for new, 💾 for save, 🗑️ for remove, navigation arrows)
- **Button Width**: Toolbar buttons use width=3 for consistency
- **Tooltips**: Implement tooltips for all toolbar buttons using `create_tooltip` method
- **Entry Fields**: Use appropriate widths based on content type (10 for IDs, 20-50 for text)

### Treeview Configuration
- **Column Setup**: Always use `show="headings"` and define column tuples
- **Column Sizing**: Set width, minwidth, and anchor for each column
- **Scrollbar**: Always include vertical scrollbar with proper configuration
- **Selection Binding**: Use `<ButtonRelease-1>` or `<<TreeviewSelect>>` for selection events

## Database Interaction Patterns

### Connection Management
- **Connection Method**: Use `self.conectar()` from BaseWindow for database connections
- **Transaction Pattern**: Use try/except blocks with proper rollback on errors
- **Resource Cleanup**: Always close connections in finally blocks

### CRUD Operations
- **Insert Pattern**: Use `get_next_recnum()` utility for new records
- **Update Pattern**: Check `current_id` or `current_recnum` to determine insert vs update
- **Delete Pattern**: Use confirmation pattern with `request_confirmation()` method
- **Select Pattern**: Use LEFT JOIN for related data, ORDER BY for consistent results

### Record Number Management
- **Recnum Generation**: Always use `self.get_next_recnum(table_name)` for new records
- **State Tracking**: Use `self.set_current_recnum()` and `self.clear_record_state()` methods
- **Validation**: Validate recnum before database operations

## Navigation and User Interaction

### Navigation Controls
- **Standard Buttons**: First (⏮), Previous (◀), Next (▶), Last (⏭)
- **Navigation Methods**: Implement `ir_primeiro`, `ir_anterior`, `ir_proximo`, `ir_ultimo`
- **Tree Navigation**: Use `tree.selection_set()`, `tree.focus()`, `tree.see()` for selection

### Message System
- **Message Types**: Use "info" (blue), "success" (green), "warning" (orange), "error" (red)
- **Auto-clear**: Non-error messages auto-clear after 5 seconds
- **Consistent Format**: Use `self.show_message(message, msg_type)` pattern

### Confirmation Pattern
- **Two-step Confirmation**: Use `setup_confirmation_pattern()` and `request_confirmation()`
- **Action Names**: Use descriptive action names like 'save', 'remove'
- **Timeout**: Default 3-second timeout for confirmation reset

## Data Handling Standards

### Form Validation
- **Required Fields**: Check mandatory fields before save operations
- **Data Types**: Use safe conversion methods for numeric values
- **Error Handling**: Display specific error messages for validation failures

### Combo Box Management
- **Data Loading**: Load combo data in constructor with dedicated methods
- **Value Mapping**: Store ID-name pairs for combo box selections
- **Selection Handling**: Use `next()` with generator expressions to find IDs from names

### Field Clearing and Population
- **Clear Pattern**: Implement `limpar()` method to clear all form fields
- **Population Pattern**: Use `delete(0, tk.END)` followed by `insert(0, value)`
- **State Reset**: Clear both `current_id` and `current_recnum` when clearing forms

## Error Handling and Logging

### Exception Management
- **Database Errors**: Catch `sqlite3.Error` and specific subtypes
- **User Feedback**: Always show meaningful error messages to users
- **Rollback**: Use `conn.rollback()` on database errors

### Logging Integration
- **Recnum Operations**: Use BaseWindow logging utilities for recnum operations
- **Debug Information**: Log state changes and important operations
- **Error Logging**: Log errors with context information

## Code Organization Principles

### Method Organization
- **Constructor**: UI setup and initialization
- **Event Handlers**: User interaction methods (novo, salvar, remover)
- **Data Methods**: Database operations (carregar_*, salvar, etc.)
- **Navigation**: Movement between records
- **Utilities**: Helper methods (create_tooltip, show_message, etc.)

### Naming Conventions
- **Variables**: Use descriptive Portuguese names (entry_nome, combo_tipo)
- **Methods**: Use Portuguese verbs (carregar, salvar, limpar, remover)
- **Constants**: Use uppercase for configuration values
- **Database Fields**: Follow existing schema naming patterns

### Code Reuse
- **Base Class Utilities**: Leverage BaseWindow methods for common operations
- **Consistent Patterns**: Use same patterns across all windows
- **Shared Components**: Reuse toolbar, message panel, and navigation patterns