# Changelog

All notable changes to Metadata Manager are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased]

---

## [0.6.3] — 2026-02-25

### Fixed
- Plugin icon in QGIS Plugin Manager now shows the Blue Miner instead of the generic green Plugin Builder icon. The `icon.svg` (Blue Miner figure) is now present at the plugin root where `metadata.txt icon=icon.svg` expects it.

---

## [0.6.2] — 2026-02-24

### Fixed
- **Scanner hang on PMTiles and web assets** — `_discover_geospatial_files()` now skips known non-geospatial extensions (`.pmtiles`, `.js`, `.html`, `.py`, `.pdf`, etc.) before calling `ogr.Open()` / `gdal.Open()`. GDAL's PMTiles driver (added in GDAL 3.8) would block in C-level I/O when scanning MapSplat output directories; the skip-list prevents this entirely. A summary of skipped files is logged.
- **Stop button non-responsive** — `stop_inventory()` now re-enables the UI immediately (does not wait for the thread), calls `runner_thread.quit()`, and force-terminates via `runner_thread.terminate()` after a 3-second timeout if the thread is still blocked in GDAL C code.
- **Cancel showed an error dialog** — the runner now emits a dedicated `canceled` signal instead of routing cancellation through the `error` signal. The widget handles `canceled` with a quiet log entry and no dialog.
- **Re-scan wipes Metadata Manager tables** — `_write_geopackage()` now uses `QgsVectorFileWriter.CreateOrOverwriteLayer` (not `CreateOrOverwriteFile`) when the output database already exists, so `metadata_cache`, `organizations`, `contacts`, and other plugin tables are preserved across re-scans.

---

## [0.6.1] — 2026-02-23

### Fixed
- Release ZIP no longer contains `__pycache__` directories from plugin subdirectories.

---

## [0.6.0] — 2025-10-07

### Added
- **Integrated Inventory Scanner** — full `inventory_miner` functionality is now built into the plugin's first tab. No separate Processing script required.
  - Scan any directory for vectors, rasters, and tables
  - Parse existing metadata from FGDC `.shp.xml`, ISO 19115/19139 `.xml`, QGIS `.qmd`, and embedded GeoPackage metadata
  - All extracted metadata flows automatically into Smart Defaults
  - Progress bar, real-time color-coded log, and Stop button
  - Update mode preserves existing `metadata_status` values
- **Background processing** — inventory scan runs in a `QThread` so the QGIS UI remains responsive
- **Auto workflow handoff** — after a scan completes, the plugin switches to the Dashboard tab and refreshes statistics automatically
- New files: `widgets/inventory_widget.py`, `processors/inventory_runner.py`, `processors/__init__.py`

### Changed
- Tab order updated to: ① Inventory → ② Dashboard → ③ Layer Browser → ④ Metadata Editor
- "Use Current Database" convenience button added to the Inventory tab

---

## [0.5.0] — 2025-10-07

### Added
- **Smart Defaults from inventory** — selecting a layer auto-populates:
  - Title (Title Case conversion: `roads_2024` → *Roads 2024*, including common abbreviations GPS, GIS, DEM, …)
  - CRS, bounding extents, geometry type, feature count
  - Field list and raster info placed in Supplemental Info
  - Any existing GIS metadata from the inventory record
- **Layer Browser widget** — filterable, sortable layer list embedded in the panel:
  - Status filter: All / Needs Metadata / Partial / Complete
  - Text search across layer name and path
  - Next / Previous navigation buttons with position indicator
  - Auto-save before navigation
- `DatabaseManager.get_smart_defaults()` with comprehensive field mapping
- `MetadataWizard._convert_smart_defaults_to_metadata()` for format conversion

### Changed
- Three-tab interface: Dashboard → Layer Browser → Metadata Editor

---

## [0.4.1] — 2025-10-06

### Fixed
- Metadata XML export to `.qmd` files now uses `writeMetadataXml()` with `QDomDocument` instead of the non-existent `toXml()` method. `.qmd` files now write correctly.
- Verified working with Excel file layers (`.xls`)

---

## [0.4.0] — 2025-10-06

### Added
- **Metadata file writing** — metadata now actually saves to disk:
  - New `MetadataWriter` class handles all file write operations
  - `.qmd` sidecar files for shapefiles, GeoTIFFs, and other non-GeoPackage formats
  - Embedded metadata in GeoPackage layers via the QGIS API
  - Automatic format detection (GeoPackage → embedded; everything else → `.qmd`)
- Multi-layer container support — creates `{container}_{layer}.qmd` files for GeoPackages with multiple layers
- Write status tracking: `last_written_date`, `target_location`, `in_sync` columns in `metadata_cache`

### Changed
- Save workflow: cache first (backup), then write to target, then update inventory status
- `layer_selector_dialog.py` returns file format information

### Fixed
- Layer selector now returns file format
- Format tracking added to wizard
- Metadata status bug for container files

---

## [0.3.6] — 2025-10-06

### Fixed
- **Critical:** Database connection now loads the SpatiaLite extension, resolving *"no such function: ST_IsEmpty"* errors on metadata save
  - Tries `mod_spatialite` then `libspatialite`; falls back to QGIS install path on Windows
  - Graceful warning if SpatiaLite cannot be loaded
- Inventory status updates work correctly after metadata save
- Dashboard statistics update after save

---

## [0.3.5] — 2025-10-06

### Changed
- Dashboard now refreshes automatically when metadata is saved — no manual **Refresh Statistics** click required
- Enhanced logging for inventory status updates (✅ success marker, similar-path hint for missing layers)

---

## [0.3.4] — 2025-10-06

### Fixed
- **Critical:** `metadata_cache` column name mismatches that blocked all metadata saves:
  - `created_date` (was `created_datetime`)
  - `last_edited_date` (was `modified_datetime`)
  - `layer_name` added to `INSERT` statement
- `get_priority_recommendations` column names corrected (`parent_directory`, `format`)

---

## [0.3.3] — 2025-10-06

### Changed
- Dashboard table row height reduced to 16 px for compact display
- Vertical header hidden (consistent with wizard 18 px rows)

---

## [0.3.2] — 2025-10-06

### Fixed
- Dashboard statistics column name mismatches (`parent_directory`, `format`, `crs_authid`, `file_path`)
- All drill-down tabs now display data correctly (By Directory, By File Format, By CRS)
- Layer selector dialog column names corrected
- `metadata_status` now saves correctly via inventory update query

---

## [0.3.1] — 2025-10-06

### Added
- Plugin loads without requiring a database on startup
- Dashboard database selection controls: **Select Database…** button, connection status indicator (green/red), path label, ability to change databases mid-session

### Changed
- Wizard shows a helpful message when the user tries to select a layer without a database connected
- Wizard auto-clears when the database changes; `clear_data()` methods added to all wizard steps

---

## [0.3.0] — 2025-10-06

### Added
- **Full 4-Step Metadata Wizard:**
  - Step 1: Title, abstract, keywords, category
  - Step 2: Contacts, license, constraints, language, attribution
  - Step 3: Lineage, purpose, links, update frequency, spatial resolution
  - Step 4: HTML summary with completeness indicator (Complete / Partial)
- Database persistence: save to cache as JSON, load on layer select, update inventory tracking fields
- Contact and link management dialogs
- Compact 18 px table rows, color-coded status indicators
- Next / Previous / Skip / Save navigation

---

## [0.2.0] — 2025-10-05

### Added
- **Core database architecture:**
  - `DatabaseManager` with connection, validation, and initialization
  - Dual version tracking (`inventory_schema_version` + `metadata_schema_version`)
  - Schema migration system
  - Automatic database selection and persistence
  - Integration with Inventory Miner v0.2.0+
- **Metadata Quality Dashboard:**
  - Overall completion statistics with progress bar
  - Drill-down views: By Directory, By Data Type, By File Format, By CRS
  - Priority recommendations panel
  - Color-coded feedback (green / orange / red)
  - Refresh button

---

## [0.1.0] — 2025-10-05

### Added
- Initial plugin scaffold via QGIS Plugin Builder
- Dockable widget interface
- Plugin structure ready for metadata management implementation
