# Metadata Manager — Installation Guide

## Quick Installation

### Option A — Install from ZIP (easiest)

1. Download `MetadataManager.zip` from the [latest release](https://github.com/johnzastrow/metadatamgr/releases/latest).
2. In QGIS: **Plugins → Manage and Install Plugins → Install from ZIP**
3. Browse to `MetadataManager.zip` → **Install Plugin**
4. Go to the **Installed** tab and enable **Metadata Manager**

---

### Option B — Install from source

**Clone the repository**
```bash
git clone https://github.com/johnzastrow/metadatamgr.git
cd metadatamgr
```

**Compile Qt resources** (required before first use)
```bash
pyrcc5 -o resources.py resources.qrc
```

**Run the installer script**

*Windows (Command Prompt):*
```cmd
install.bat
```

*Linux / macOS:*
```bash
chmod +x install.sh
./install.sh
```

*Or use make:*
```bash
make deploy
```

**Enable in QGIS:**
1. Plugins → Manage and Install Plugins
2. Click the **Installed** tab
3. Tick **Show experimental plugins** in Settings if the plugin doesn't appear
4. Check the box next to **Metadata Manager**
5. Click the toolbar button or Plugins → Metadata Manager

---

## Manual File Copy

If the scripts don't work, copy files by hand.

### Step 1: Locate your QGIS plugin directory

| Platform | Path |
|----------|------|
| Windows | `%APPDATA%\QGIS\QGIS3\profiles\<profile>\python\plugins\` |
| Linux | `~/.local/share/QGIS/QGIS3/profiles/<profile>/python/plugins/` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/<profile>/python/plugins/` |

Replace `<profile>` with your profile name (usually `default`).

### Step 2: Copy the plugin files

Create a folder named `MetadataManager` inside the plugins directory.
Copy the following from your cloned repo into it:

```
MetadataManager/
├── __init__.py
├── MetadataManager.py
├── MetadataManager_dockwidget.py
├── MetadataManager_dockwidget_base.ui
├── fix_metadata_status.py
├── metadata.txt
├── icon.png
├── resources.py        ← compile this first: pyrcc5 -o resources.py resources.qrc
├── resources.qrc
├── db/                 ← CRITICAL — do not omit
│   ├── __init__.py
│   ├── manager.py
│   ├── metadata_writer.py
│   ├── migrations.py
│   └── schema.py
├── processors/         ← CRITICAL — do not omit
│   ├── __init__.py
│   ├── inventory_processor.py
│   └── inventory_runner.py
├── widgets/            ← CRITICAL — do not omit
│   ├── __init__.py
│   ├── dashboard_widget.py
│   ├── inventory_widget.py
│   ├── layer_list_widget.py
│   ├── layer_selector_dialog.py
│   └── metadata_wizard.py
├── icons/
└── i18n/
```

> The `db/`, `processors/`, and `widgets/` subdirectories are required. The plugin will fail to load if any are missing.

---

## First Use

1. **Open the plugin** — click the Metadata Manager toolbar button or Plugins menu.

2. **Connect a database** — on the **Dashboard** tab click **Select Database…** and choose a `.gpkg` file.
   - If you already have a database created by **Inventory Miner**, select that file. The plugin will add its own tables to it automatically.
   - If you don't have one yet, go to the **Inventory** tab, point it at a directory, and run a scan. The scan creates the database.

3. **Scan your data** (optional — skip if you have an Inventory Miner database)
   - On the **Inventory** tab, browse to your data root directory
   - Choose an output GeoPackage path
   - Click **Start Scan**

4. **Review the dashboard** — the **Dashboard** tab shows overall completion and priority recommendations immediately after connecting.

5. **Start adding metadata** — switch to **Layer Browser**, filter by *Needs Metadata*, and double-click any row to open it in the wizard.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| *"This plugin is broken"* | Missing subdirectories in install | Re-run `install.bat`/`install.sh` or copy `db/`, `processors/`, `widgets/` manually |
| Plugin missing from menu | Not enabled | Plugins → Manage → Installed → check Metadata Manager |
| *"Not connected to database"* | No database selected | Click **Select Database…** on the Dashboard tab |
| *"Invalid database"* | File was not created by Inventory Miner 0.2.0+ | Use the built-in scanner on the Inventory tab to create a new database |
| Import errors for `db`/`widgets` | Subdirectories not copied | Copy `db/`, `processors/`, `widgets/` to the plugin directory |
| *"no such function: ST_IsEmpty"* | SpatiaLite extension not loaded | Ensure QGIS GDAL build includes SpatiaLite |

---

## Uninstallation

1. Disable the plugin in Plugin Manager
2. Close QGIS
3. Delete the plugin folder:

```bash
# Linux / macOS
rm -rf ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/MetadataManager

# Windows (Command Prompt)
rmdir /s "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\MetadataManager"
```

---

## Version information

- **Current release:** 0.6.4
- **QGIS minimum:** 3.40
- **Repository:** https://github.com/johnzastrow/metadatamgr
- **Issues:** https://github.com/johnzastrow/metadatamgr/issues
