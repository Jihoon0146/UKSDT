# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Windows Git Bash)
source ./venv/Scripts/activate

# Set environment variables
export UKSDT_RESOURCE_PATH="./resources"
```

### UI Development
```bash
# Update all UI files from .ui to _ui.py (run after modifying .ui files)
./update_ui.sh

# Run the application
./run.sh
# Or manually:
./venv/Scripts/python.exe ./src/main.py
```

### Dependencies
- Install requirements: `pip install -r requirements.txt`
- Main dependencies: PyQt5, QDarkStyle, pandas, python-dateutil

## Architecture Overview

### Application Structure
- **PyQt5-based desktop application** with tabbed interface and collapsible sidebar
- **Main entry point**: `src/main.py` - sets up QApplication with custom theme and fonts
- **Main window**: `src/core/main_window.py` - manages sidebar, custom tab widget, and tool loading
- **Tools are loaded as plugins** into tabs when selected from sidebar

### Core Components
- **MainWindowUI**: Central window with splitter layout (sidebar + content area)
- **CollapsibleSidebarUI**: Left navigation panel for tool selection
- **CustomTabWidget**: Enhanced tab widget with closable, movable tabs
- **Tool Widgets**: Each tool (Control DR Reviewer, Projects, Externals) is a separate QWidget

### Tool Architecture
Each tool follows the pattern:
```
src/tools/{tool_name}/
├── {tool_name}.py              # Main widget class
├── {tool_name}.ui              # Qt Designer file  
├── {tool_name}_ui.py           # Generated UI code
└── components/                 # Tool-specific components
    ├── {component}.py
    ├── {component}.ui
    └── {component}_ui.py
```

### UI Generation Workflow
1. Design interfaces in Qt Designer (.ui files)
2. Run `./update_ui.sh` to convert .ui files to Python code (_ui.py)
3. Python classes inherit from generated UI classes

### Resource Management
- **Environment variable**: `UKSDT_RESOURCE_PATH` points to `./resources`
- **Resources structure**:
  - `data/`: JSON configuration files and schemas
  - `fonts/`: LG custom fonts (LGEITextTTF, LGEIHeadlineTTF)
  - `icons/`: UI icons organized by category
  - `styles/`: QSS stylesheets (ElegantDark.qss)
  - `templates/`: Export templates for Excel/PDF

### Key Tools
1. **Control DR Reviewer** (`src/tools/control_dr_reviewer/`):
   - File upload and verification tool for BOM and SW test files
   - Uses pandas for Excel processing
   - Generates reports and exports to Excel

2. **Projects** (`src/tools/projects/`):
   - Advanced project management with hierarchical structure (Wrappers > Projects)
   - Dual-mode UI: Project detail view and Wrapper detail view
   - Smart completion workflow with automatic wrapper completion suggestions
   - Context menu support for CRUD operations (add, delete projects/wrappers)
   - JSON-based data storage with schema validation
   - MVC pattern with DataModel, TreeBuilder, DetailView components

3. **Externals** (`src/tools/externals/`):
   - External links management with grid layout
   - Loads links from JSON configuration
   - Supports favoriting and categorization

### Data Management
- **Projects data**: `resources/data/projects.sample.json` with JSON Schema validation
- **External links**: `resources/data/external_links.json`
- **Configuration-driven** approach for easy customization

### Theming and Styling
- **QDarkStyle** as primary theme with custom QSS overrides
- **Custom LG fonts** automatically loaded and applied
- **High DPI support** enabled for modern displays

## Key Features

### Projects Tool Advanced Features
- **Hierarchical Project Management**: Two-tier structure (Wrappers contain Projects)
- **Right-click Context Menus**: 
  - Status roots: Add Wrapper/Project
  - Wrappers: Add Project, Delete Wrapper, Show Details
  - Projects: Delete Project
- **Smart Completion System**:
  - Projects can only be completed via "완료" button
  - Automatic wrapper completion check when all child projects are completed
  - Manual wrapper completion via dedicated wrapper detail view
- **Dual Detail Views**:
  - **Project Detail**: Standard form with read-only status, completion button
  - **Wrapper Detail**: Overview dashboard with progress bar, child project list, completion management
- **Tree View Enhancements**:
  - Completed section automatically collapsed on startup
  - Dynamic tree restructuring on status changes
  - Visual status indicators (🟢 진행 중, 🔴 완료, 📚 wrapper, 📗📕 projects)

### Development Workflow for Projects Tool
1. **Adding Items**: Right-click → context menu → Add Wrapper/Project → name input → immediate save (Wrapper) or temp add + detail edit (Project)
2. **Completion Flow**: Project detail → "완료" button → confirmation → status change → tree update → wrapper auto-check
3. **Wrapper Management**: Click wrapper → detail view → progress overview → completion button (if eligible)
4. **Data Persistence**: All changes immediately saved to JSON with automatic tree refresh

### Important Implementation Notes
- **UI Generation**: Always run `./update_ui.sh` after modifying .ui files
- **Resource Path**: Set `UKSDT_RESOURCE_PATH="./resources"` before running
- **State Management**: Project status changes only via completion buttons, not direct editing
- **Safety Checks**: Wrapper deletion blocked if child projects exist
- **ID Generation**: Timestamp-based unique IDs for new items