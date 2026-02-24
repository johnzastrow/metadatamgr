# Metadata Manager

> A QGIS plugin for creating, managing, and tracking geospatial layer metadata — with integrated inventory scanning, a guided 4-step wizard, smart defaults, and a quality dashboard.

[![Version](https://img.shields.io/badge/version-0.6.1-blue)](https://github.com/johnzastrow/metadatamgr/releases)
[![QGIS](https://img.shields.io/badge/QGIS-3.40%2B-green)](https://qgis.org)
[![License](https://img.shields.io/badge/license-GPL--2.0-orange)](LICENSE)
[![Status](https://img.shields.io/badge/status-experimental-yellow)](https://github.com/johnzastrow/metadatamgr/releases)

---

![.]{icons/icon.png)

## Overview

**Metadata Manager** is a QGIS dockable panel that turns metadata creation from a chore into a streamlined workflow. It combines a built-in directory scanner, a reusable component library (organizations, contacts, keywords), and a progressive disclosure wizard into one panel — eliminating the back-and-forth between tools.

The key idea is a **unified GeoPackage database** shared with the [Inventory Miner](https://github.com/johnzastrow/mqs/tree/main/Scripts/inventory_miner.py) script. Inventory Miner catalogs your geospatial files; Metadata Manager adds metadata management tables to the same `.gpkg` and updates each layer's status as you work.

### What it replaces

| Before | After |
|--------|-------|
| Run a separate script to catalog data | Built-in scanner on the Inventory tab |
| Open each layer's properties to edit metadata | Layer Browser with Next/Previous navigation |
| Type titles and CRS manually | Smart Defaults auto-populate from the inventory |
| Guess which layers need attention | Quality Dashboard shows completion by directory/format/CRS |
| Keep metadata in your head | All metadata cached in the database with sync tracking |

---

## Screenshots

| Dashboard | Inventory Scanner |
|-----------|-------------------|
| ![Dashboard statistics](docs/images/mmdashboard.png) | ![Inventory scan UI](docs/images/mmscan.png) |

| Metadata Editor — Step 2 | Output targets |
|--------------------------|----------------|
| ![Wizard step 2](docs/images/mmstep2.png) | ![Output files](docs/images/mmoutputs.png) |

---

## Features

### ① Integrated Inventory Scanner
- Scan any directory tree for geospatial files (vectors, rasters, tables)
- Parses existing metadata from FGDC `.xml`, ISO 19115 `.xml`, QGIS `.qmd`, and embedded GeoPackage metadata
- Runs in a background thread — UI stays responsive
- Update mode preserves existing `metadata_status` values
- All results flow directly into the Smart Defaults for the wizard

### ② Metadata Quality Dashboard
- Overall completion percentage with a progress bar
- Drill-down by **Directory**, **Data Type**, **File Format**, and **CRS**
- Priority recommendations: highlights where effort has the most impact
- Color-coded status indicators (complete / partial / none)
- Database connection indicator with path label

### ③ Layer Browser
- Filterable list of all inventory layers: All / Needs Metadata / Partial / Complete
- Text search across layer names and paths
- Next / Previous navigation — auto-saves before moving to the next layer
- Position indicator ("Layer 5 of 42")

### ④ Metadata Editor Wizard (4 steps)
| Step | Fields | Required? |
|------|--------|-----------|
| 1 — Essential | Title, Abstract, Keywords, Category | Yes |
| 2 — Common | Contacts, License, Constraints, Language, Attribution | Recommended |
| 3 — Optional | Lineage, Purpose, Links, Update Frequency, Resolution | No |
| 4 — Review | HTML preview, completeness indicator, Save | — |

**Smart Defaults** auto-populate from the inventory when a layer is selected:
- Title (converted to Title Case: `roads_2024` → *Roads 2024*)
- CRS, bounding extent, geometry type, feature count, raster dimensions
- Any existing GIS metadata already in the file

### Metadata Writing
Metadata is written to the appropriate target automatically:

| Source type | Target |
|-------------|--------|
| GeoPackage layer | Embedded metadata (via `QgsLayerMetadata` API) |
| Shapefile, GeoTIFF, etc. | `.qmd` sidecar file in the same directory |
| All layers | Cached as JSON in the database (backup/recovery) |

### Reusable Library
The database stores reusable components you define once and reuse across layers:
- **Organizations** — full contact details (address, email, phone, website)
- **Contacts** — named contacts with ISO 19115 roles (author, custodian, pointOfContact, …)
- **Keywords** — hierarchical keyword library with vocabulary tracking
- **Keyword Sets** — themed collections for bulk application
- **Templates** — save and reapply complete or partial metadata profiles

---

## Requirements

| Requirement | Version |
|-------------|---------|
| QGIS | 3.40 or higher |
| Python | 3.9+ (bundled with QGIS) |
| GDAL / OGR | Any version bundled with QGIS |
| pyrcc5 | For building from source only |

No external Python packages are required. The plugin uses only PyQGIS, PyQt, and the Python standard library.

> **First-time setup note:** The plugin expects a GeoPackage database created by [Inventory Miner](https://github.com/johnzastrow/mqs/tree/main/Scripts/inventory_miner.py) (`geospatial_inventory` table must exist). You can also use the built-in scanner on the Inventory tab to create one without the separate script.

---

## Installation

### Option A — Install from ZIP (recommended)

1. Download `MetadataManager.zip` from the [latest release](https://github.com/johnzastrow/metadatamgr/releases/latest).
2. In QGIS: **Plugins → Manage and Install Plugins → Install from ZIP**
3. Browse to `MetadataManager.zip` and click **Install Plugin**.
4. Enable the plugin on the **Installed** tab.

### Option B — Install from source

**Clone the repo**
```bash
git clone https://github.com/johnzastrow/metadatamgr.git
cd metadatamgr
```

**Compile Qt resources** (required once, and after editing `resources.qrc`)
```bash
pyrcc5 -o resources.py resources.qrc
```

**Deploy to your QGIS profile**

*Windows (Command Prompt):*
```cmd
install.bat
```

*Linux / macOS:*
```bash
./install.sh
```

*Or use make:*
```bash
make deploy
```

**Enable in QGIS:** Plugins → Manage and Install Plugins → Installed tab → check **Metadata Manager**

### Plugin directory locations

| Platform | Path |
|----------|------|
| Windows | `%APPDATA%\QGIS\QGIS3\profiles\<profile>\python\plugins\MetadataManager\` |
| Linux | `~/.local/share/QGIS/QGIS3/profiles/<profile>/python/plugins/MetadataManager/` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/<profile>/python/plugins/MetadataManager/` |

Replace `<profile>` with your profile name (usually `default`).

---

## Quick Start

### First time

1. **Run the scanner** — open the **Inventory** tab, point it at your data directory, and click Scan. This creates or updates the inventory in a GeoPackage file you choose.
   - *Already have an Inventory Miner database?* Skip to step 2.

2. **Connect the database** — on the **Dashboard** tab, click **Select Database…** and choose your `.gpkg` file. The plugin validates it and creates its own tables automatically.

3. **Review the dashboard** — see overall completion and the priority recommendations panel.

4. **Pick a layer** — switch to the **Layer Browser** tab, filter by *Needs Metadata*, and double-click any row.

5. **Fill in the wizard** — Step 1 fields are pre-filled from the inventory. Add an abstract and any keywords, then click **Save** or **Next →** to advance to the next layer.

### Typical batch workflow

```
Dashboard → see "40 shapefiles in /project_a/ have no metadata"
Layer Browser → filter: format=Shapefile, directory=/project_a/
→ work through them with Next / Previous
→ dashboard updates in real time as layers move to 'complete'
```

---

## Architecture

### Unified database

Both Metadata Manager and the Inventory Miner script share a single GeoPackage:

```
geospatial_catalog.gpkg
├── geospatial_inventory   ← created by Inventory Miner / built-in scanner
├── metadata_cache         ← created by Metadata Manager
├── organizations          ←      "
├── contacts               ←      "
├── keywords               ←      "
├── keyword_sets           ←      "
├── keyword_set_members    ←      "
├── templates              ←      "
├── settings               ←      "
├── plugin_info            ← shared version tracking
└── upgrade_history        ← schema migration log
```

The `geospatial_inventory` table has 66+ fields. Metadata Manager only writes to the metadata-specific columns (`metadata_status`, `metadata_last_updated`, `metadata_target`, `metadata_cached`) — it never touches the file catalog columns owned by Inventory Miner.

### Schema versioning

`plugin_info` holds two independent version keys:
- `inventory_schema_version` — owned by Inventory Miner
- `metadata_schema_version` — owned by Metadata Manager

Each tool upgrades only its own tables. Migration history is logged in `upgrade_history`.

### metadata_cache JSON structure

```json
{
  "title": "Roads 2024",
  "abstract": "Transportation network for the study area...",
  "keywords": ["roads", "transportation", "2024"],
  "categories": ["transportation"],
  "language": "ENG",
  "crs": "EPSG:4326",
  "extent": { "xmin": -94.1, "ymin": 44.2, "xmax": -89.5, "ymax": 47.8 },
  "contacts": [
    { "name": "Jane Smith", "role": "pointOfContact", "organization": "Acme GIS" }
  ],
  "links": [
    { "name": "Data Portal", "url": "https://example.org/data", "type": "WWW:LINK" }
  ],
  "constraints": { "access": "Public", "use": "CC-BY-4.0" },
  "licenses": ["CC-BY-4.0"]
}
```

### Module map

```
metadatamgr/
├── __init__.py                     QGIS entry point (classFactory)
├── MetadataManager.py              Plugin lifecycle, toolbar, menu
├── MetadataManager_dockwidget.py   Main dock panel, tab management
├── MetadataManager_dockwidget_base.ui  Qt Designer layout
│
├── db/
│   ├── schema.py                   Table definitions
│   ├── manager.py                  Connection, queries, smart defaults
│   ├── migrations.py               Schema upgrade system
│   └── metadata_writer.py          Write to .qmd / GeoPackage
│
├── widgets/
│   ├── inventory_widget.py         Tab 1 — scanner UI + progress
│   ├── dashboard_widget.py         Tab 2 — statistics and drill-downs
│   ├── layer_list_widget.py        Tab 3 — filterable layer browser
│   ├── metadata_wizard.py          Tab 4 — 4-step wizard
│   └── layer_selector_dialog.py    Layer picker dialog
│
└── processors/
    ├── inventory_processor.py      Core directory scanning logic (GDAL/OGR)
    └── inventory_runner.py         Background QThread wrapper
```

---

## Development

### Prerequisites

- QGIS 3.40+ with PyQGIS
- `pyrcc5` (comes with `pyqt5-dev-tools`)
- `pytest` for running unit tests

### Build commands

```bash
# Compile Qt resources (run once, and after editing resources.qrc)
make compile          # or: pyrcc5 -o resources.py resources.qrc

# Deploy to default QGIS profile
make deploy

# Run tests
make test             # or: python -m pytest test/ -v

# Create distributable ZIP
make package          # produces MetadataManager.zip

# Remove deployed plugin
make remove

# Clean compiled/cache files
make clean
```

### Running tests

Only `test/test_inventory_processor_unit.py` runs without a live QGIS instance. The other tests in `test/` use the Plugin Builder scaffold and require a QGIS environment.

```bash
# Unit test only (CI-safe)
python -m pytest test/test_inventory_processor_unit.py -v

# All tests (requires QGIS Python environment)
python -m pytest test/ -v
```

A `conftest.py` at the repo root installs `_AutoMockModule` stubs for `qgis.*` and `osgeo.*` so the unit test can be collected and run without QGIS installed.

### Release process

Releases are built automatically by GitHub Actions when a version tag is pushed:

```bash
# Bump version in metadata.txt and all module __version__ strings, then:
git tag v0.7.0
git push origin v0.7.0
```

The workflow (`.github/workflows/release.yml`) will:
1. Compile `resources.py`
2. Run `test/test_inventory_processor_unit.py`
3. Build `MetadataManager.zip` (production files only, no `__pycache__`)
4. Extract the matching changelog section from `docs/CHANGELOG.md`
5. Publish a GitHub Release with the ZIP attached

---

## Troubleshooting

| Error | Likely cause | Fix |
|-------|-------------|-----|
| *"This plugin is broken"* on enable | Missing `db/` or `widgets/` dirs | Re-run `install.bat` / `install.sh` |
| *"Not connected to database"* | No database selected yet | Click **Select Database…** on Dashboard tab |
| *"Invalid database"* on connect | Database not created by Inventory Miner 0.2.0+ | Re-run Inventory Miner or use the built-in scanner |
| Import errors for `db` or `widgets` | Subdirectories missing from install | Copy `db/`, `widgets/`, `processors/` manually |
| Plugin not in menu | Not enabled in Plugin Manager | Plugins → Manage → Installed → check Metadata Manager |
| *"no such function: ST_IsEmpty"* | SpatiaLite extension failed to load | Ensure QGIS GDAL build includes SpatiaLite; check QGIS version |

---

## Changelog

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for the full history.

| Version | Highlights |
|---------|-----------|
| **0.6.1** | Release ZIP cleanup |
| **0.6.0** | Built-in inventory scanner — no separate script needed |
| **0.5.0** | Smart Defaults, Layer Browser with Next/Previous navigation |
| **0.4.0** | Metadata writing to `.qmd` and GeoPackage |
| **0.3.0** | Full 4-step Metadata Wizard |
| **0.2.0** | Database architecture, Quality Dashboard |
| **0.1.0** | Initial plugin scaffold |

---

## License

[GPL-2.0](LICENSE) — same license as QGIS itself.

---

## Related tools

- **[Inventory Miner](https://github.com/johnzastrow/mqs/tree/main/Scripts/inventory_miner.py)** — QGIS Processing script that scans directories and creates the GeoPackage inventory that this plugin reads and writes to. Run it first (or use the built-in scanner).
- **[MapSplat](https://github.com/johnzastrow/mapsplat)** — sister plugin that exports QGIS projects to static web maps using PMTiles and MapLibre GL JS.
