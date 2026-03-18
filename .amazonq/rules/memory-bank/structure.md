# Alba System - Project Structure

## Directory Organization

### Root Level Files
- `main.py` - Application entry point and main window with MDI container
- `mdi.py` - Multiple Document Interface container implementation
- `estilo.py` - Global styling and theme configuration
- `requirements.txt` - Python dependencies (ttkbootstrap)
- `README.md` - Build and configuration instructions

### Core Directories

#### `/windows/` - Business Module Windows
Contains all business logic windows and forms:

**Administrative Modules:**
- `usuarios.py` - User management
- `system_config.py` - System configuration
- `empresas.py` - Company management

**Customer & Contact Management:**
- `pessoas.py` - Person/customer management
- `contatos.py` - Contact information management
- `endereco.py` - Address management
- `tipo.py` - Customer type classification

**Geographic & Fiscal Data:**
- `cep.py` - Postal code management
- `ncm.py` - NCM tax classification codes
- `cfop.py` - CFOP fiscal operations
- `natop.py` - Nature of operations
- `tiponf.py` - Invoice type management
- `ativid.py` - Business activity types

**Product & Inventory:**
- `produto_fiscal.py` - Fiscal product management
- `grupo_produtos.py` - Product group organization
- `itens_producao.py` - Production item tracking

**Financial Operations:**
- `orcamento.py` - Budget/quotation management
- `ordem_compra.py` - Purchase order management
- `item_ordem_compra.py` - Purchase order items
- `ordens_faturamento.py` - Billing order management
- `nota_fiscal.py` - Invoice management
- `item_nota_fiscal.py` - Invoice item management
- `comissao.py` - Commission management

**Utilities:**
- `base_window.py` - Base window class with common functionality
- `textos.py` - Text template management

#### `/alba_zip_extracted/` - Database
- `alba.sqlite` - SQLite database file

#### `/.amazonq/` - Development Tools
- `/rules/memory-bank/` - Project documentation and guidelines

#### `/.kiro/` - Project Management
- `/specs/` - Feature specifications and requirements
- `/steering/` - Project steering documentation

## Architectural Patterns

### Window Architecture
- **Base Class Pattern**: All windows inherit from `BaseWindow` class
- **MDI Pattern**: Multiple Document Interface for window management
- **Modular Design**: Each business entity has its own dedicated window module

### Data Layer
- **SQLite Database**: Single file database for data persistence
- **Direct SQL Access**: Windows directly interact with SQLite database
- **Environment Configuration**: Database path configurable via `ALBA_DB_PATH` environment variable

### UI Framework
- **ttkbootstrap**: Modern themed Tkinter widgets
- **Consistent Styling**: Global styling applied via `estilo.py`
- **Responsive Layout**: Frames and containers for flexible layouts

### Navigation Patterns
- **CRUD Operations**: Create, Read, Update, Delete functionality in each module
- **Record Navigation**: First, Previous, Next, Last navigation controls
- **Search Functionality**: Built-in search capabilities
- **Toolbar Actions**: Standardized toolbar with common operations

## Component Relationships

### Core Dependencies
```
main.py → mdi.py → windows/*.py → base_window.py
                                → estilo.py
                                → alba.sqlite
```

### Window Hierarchy
- `App` (main application) contains `MDIContainer`
- `MDIContainer` manages multiple business windows
- Each business window extends `BaseWindow`
- `BaseWindow` provides common functionality (navigation, CRUD, styling)

### Data Flow
1. User interaction in window
2. Window validates input
3. Direct SQLite database operations
4. UI updates reflect database changes
5. Message system provides user feedback