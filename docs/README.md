# Metadata Manager

A QGIS Plugin that helps users create, manage, and apply metadata to layers following QGIS and ISO 19115 standards.

**⚙️ STATUS: IN DEVELOPMENT** - Plugin structure created with QGIS Plugin Builder. Core functionality implementation in progress.

## Overview

Metadata Manager simplifies the process of creating and managing layer metadata by providing:
- **Unified database with Inventory Miner**: Uses the same GeoPackage database (e.g., `geospatial_catalog.gpkg`)
- Reusable metadata component libraries (organizations, contacts, keywords)
- Template system for bulk metadata application
- Direct integration with inventory table to identify layers lacking metadata
- Guided workflow for metadata creation with Next/Previous navigation
- Export to QGIS XML format and direct association with GeoPackage layers
- Real-time metadata status tracking in inventory table

## Installation

### From Source (Development)

1. **Copy plugin to QGIS plugins directory:**
   ```
   Windows: C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\<profile>\python\plugins\
   Linux: ~/.local/share/QGIS/QGIS3/profiles/<profile>/python/plugins/
   macOS: ~/Library/Application Support/QGIS/QGIS3/profiles/<profile>/python/plugins/
   ```

2. **Copy the entire metadata_manager directory:**
   ```bash
   cp -r Plugins/metadata_manager /path/to/qgis/plugins/
   ```

3. **Compile resources (required):**

   Option A - Using make:
   ```bash
   cd /path/to/qgis/plugins/metadata_manager
   make
   ```

   Option B - Using pb_tool:
   ```bash
   cd /path/to/qgis/plugins/metadata_manager
   pb_tool compile
   pb_tool deploy
   ```

   Option C - Manual compilation:
   ```bash
   cd /path/to/qgis/plugins/metadata_manager
   pyrcc5 -o resources.py resources.qrc
   ```

4. **Enable plugin in QGIS:**
   - Open QGIS
   - Go to Plugins → Manage and Install Plugins
   - Check "Show also experimental plugins" in Settings
   - Find "Metadata Manager" in the Installed tab
   - Check the box to enable it

5. **Access the plugin:**
   - Look for the Metadata Manager icon in the toolbar
   - Or go to Plugins menu → Metadata Manager

6. **First run setup:**
   - **IMPORTANT**: Run Inventory Miner first to create your inventory database
   - Plugin will prompt you to select your existing inventory database (e.g., `geospatial_catalog.gpkg`)
   - Plugin adds its own tables to the existing database (organizations, keywords, templates, metadata_cache)
   - Both tools share the same database for seamless integration

## Development Setup

### Prerequisites
- QGIS 3.40 or higher
- Python 3.9+
- pyrcc5 (for compiling resources)
- Optional: pb_tool (`pip install pb_tool`)

### Building and Testing

**Using Makefile:**
```bash
make          # Compile resources
make deploy   # Deploy to QGIS plugins directory
make test     # Run tests
make clean    # Clean compiled files
```

**Using pb_tool:**
```bash
pb_tool compile   # Compile resources
pb_tool deploy    # Deploy to QGIS plugins directory
pb_tool clean     # Clean compiled files
```

### Project Structure

```
Plugins/metadata_manager/
├── __init__.py                          # Plugin entry point
├── MetadataManager.py                   # Main plugin class
├── MetadataManager_dockwidget.py        # Dockable widget
├── MetadataManager_dockwidget_base.ui   # Qt Designer UI file
├── metadata.txt                         # Plugin metadata
├── icon.png                             # Plugin icon
├── resources.qrc                        # Qt resources file
├── resources.py                         # Compiled resources (generated)
├── db/                                  # Database management (planned)
│   ├── schema.py                        # Database schema definitions
│   ├── migrations.py                    # Schema upgrade scripts
│   └── manager.py                       # Database operations
├── Makefile                             # Build automation
├── pb_tool.cfg                          # pb_tool configuration
├── pylintrc                             # Code quality configuration
├── i18n/                                # Translations
├── help/                                # Help documentation
├── test/                                # Unit tests
└── scripts/                             # Helper scripts

User Data:
metadatamanager.gpkg                     # User-created database (not in repo)
```

## Planned Features

### v0.2.0 - Database and Core Metadata Management
- [ ] Unified GeoPackage database integration with Inventory Miner
- [ ] Database selection dialog (browse for existing inventory database)
- [ ] Database validation (check for geospatial_inventory table)
- [ ] Add Metadata Manager tables to existing database
- [ ] Dual version tracking (inventory_schema_version + metadata_schema_version)
- [ ] Automatic schema upgrades for Metadata Manager tables only
- [ ] Inventory Miner integration (run from within plugin)
- [ ] **Metadata Quality Dashboard**: Statistics by directory, data type, format, age, CRS with priority recommendations
- [ ] **Progressive Disclosure Wizard**: Required → Common → Optional fields with skip navigation
- [ ] **Smart Defaults from Inventory**: Auto-populate title, CRS, extent, geometry type, field list, etc.
- [ ] Metadata editor interface (wizard and expert modes)
- [ ] QGIS layer metadata integration
- [ ] Basic validation
- [ ] Save/load metadata from layers and update inventory.metadata_status

### v0.3.0 - Reusable Libraries
- [ ] Organization library (SQLite database)
- [ ] Keyword library with hierarchical organization
- [ ] Contact management
- [ ] Quick selection from saved components

### v0.4.0 - Template System
- [ ] Create metadata templates
- [ ] Save/load templates
- [ ] Apply templates to layers
- [ ] Template import/export

### v0.5.0 - Inventory Integration
- [ ] Connect to inventory GeoPackage databases
- [ ] List layers from inventory
- [ ] Filter layers by metadata status
- [ ] Batch template application

### v0.6.0 - Export and GeoPackage Integration
- [ ] Export to QGIS XML format
- [ ] Write metadata directly to GeoPackage layers
- [ ] Read metadata from GeoPackage layers
- [ ] Batch export and GeoPackage metadata operations

### v1.0.0 - Production Release
- [ ] Guided wizard mode
- [ ] Expert mode
- [ ] Auto-population from layer properties
- [ ] Comprehensive validation
- [ ] User documentation
- [ ] Stable API

## Current Status (v0.1.0)

✅ **Completed:**
- Plugin structure created with QGIS Plugin Builder
- Dockable widget interface
- Development infrastructure (Makefile, pb_tool, tests)
- Plugin metadata and configuration
- Documentation structure

🚧 **In Development:**
- Core metadata editor UI
- Database schema for libraries
- Integration with QgsLayerMetadata API

## Contributing

This is part of the MQS (My QGIS Stuff) collection. See the main repository README for contribution guidelines.

## Testing

Run tests using:
```bash
make test
```

Or manually:
```bash
cd test
python -m pytest
```

## Known Issues

- Plugin is in early development
- UI is placeholder from Plugin Builder template
- Core functionality not yet implemented

## Technical Details

See `REQUIREMENTS.md` for detailed technical specifications including:
- Metadata standards compliance
- Database schema
- UI design specifications
- Integration requirements

## Resources

- **QGIS Plugin Development**: http://loc8.cc/pyqgis_resources
- **QGIS Metadata API**: https://qgis.org/pyqgis/master/core/QgsLayerMetadata.html
- **ISO 19115**: https://www.iso.org/standard/53798.html
- **Plugin Builder**: http://g-sherman.github.io/Qgis-Plugin-Builder/

## License

MIT License - See repository root for details.

## Author

Part of the MQS (My QGIS Stuff) collection by John Zastrow.

## Version History

See `CHANGELOG.md` for detailed version history.
