# Alba System - Technology Stack

## Programming Languages and Versions
- **Python**: Primary development language
- **SQL**: Database queries and schema management
- **Markdown**: Documentation and specifications

## Core Dependencies

### UI Framework
- **ttkbootstrap 1.12.2**: Modern themed Tkinter widgets
  - Provides enhanced styling and modern look
  - Bootstrap-inspired themes
  - Extended widget set beyond standard Tkinter

### Standard Library Dependencies
- **tkinter**: Base GUI framework (Python standard library)
- **sqlite3**: Database connectivity (Python standard library)

## Database Technology
- **SQLite**: Embedded database engine
  - Single file database (`alba.sqlite`)
  - No server setup required
  - ACID compliant transactions
  - Configurable via `ALBA_DB_PATH` environment variable

## Build and Deployment

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# With custom database path
export ALBA_DB_PATH=/custom/path/alba.sqlite
python main.py
```

### Production Build
```bash
# Create executable using cx_Freeze
cxfreeze.exe .\main.py --target-dir .\dist\ --base-name=Win32GUI
```

## Development Tools and Configuration

### Project Management
- **Kiro Framework**: Project specifications and task management
  - `/specs/` - Feature specifications
  - `/steering/` - Project documentation
  - `/hooks/` - Development hooks

### Code Organization
- **Modular Architecture**: Separate modules for each business entity
- **Base Classes**: Common functionality through inheritance
- **Consistent Patterns**: Standardized CRUD operations across modules

### Environment Configuration
- **Database Path**: Configurable via environment variable
- **Default Path**: `alba_zip_extracted/alba.sqlite`
- **Theme**: Flatly theme from ttkbootstrap

## Development Commands

### Running the Application
```bash
python main.py
```

### Installing Dependencies
```bash
pip install ttkbootstrap==1.12.2
```

### Building Executable
```bash
cxfreeze.exe .\main.py --target-dir .\dist\ --base-name=Win32GUI
```

## System Requirements
- **Operating System**: Windows (primary target), cross-platform capable
- **Python Version**: Compatible with ttkbootstrap requirements
- **Database**: SQLite support (included in Python standard library)
- **GUI**: Tkinter support (included in Python standard library)

## Architecture Decisions
- **Single File Database**: SQLite for simplicity and portability
- **Direct SQL Access**: No ORM layer for performance and simplicity
- **MDI Interface**: Multiple Document Interface for professional business application feel
- **Modular Windows**: Each business entity in separate module for maintainability