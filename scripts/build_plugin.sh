#!/usr/bin/env bash
# Build the Metadata Manager QGIS plugin zip for upload to plugins.qgis.org.
#
# This is the CANONICAL local build — it stages exactly what the CI release workflow
# (.github/workflows/release.yml) ships, so the zip you upload matches what's tagged.
# The plugin imports subpackages (db/, processors/, widgets/), so those MUST be included;
# a pb_tool/`make` build that omits them produces a zip that fails to load.
#
# Usage:  scripts/build_plugin.sh   ->   ./MetadataManager.zip
#
# Requires: zip, and pyrcc5 (PyQt5 dev tools) to compile resources.qrc -> resources.py.
# Run it with QGIS's Python on PATH (OSGeo4W shell on Windows) so pyrcc5 is available.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

PLUGIN="MetadataManager"
OUT="$ROOT/$PLUGIN.zip"
WORK="$(mktemp -d)"
STAGE="$WORK/$PLUGIN"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$STAGE"

# 1. Root-level Python source. (Icons load from plain file paths under icons/, so there is
#    NO compiled Qt resource step — no pyrcc5, no generated resources.py.)
for f in __init__.py MetadataManager.py MetadataManager_dockwidget.py fix_metadata_status.py; do
  cp "$ROOT/$f" "$STAGE/$f"
done

# 2. UI, metadata, icons, license, docs (LICENSE is required by plugins.qgis.org).
for f in MetadataManager_dockwidget_base.ui metadata.txt icon.png icon.svg README.md LICENSE; do
  cp "$ROOT/$f" "$STAGE/$f"
done

# 4. Subpackages the plugin imports + supporting asset dirs.
for d in db processors widgets icons i18n; do
  cp -r "$ROOT/$d" "$STAGE/$d"
done

# 5. Strip caches / VCS / compiled artefacts (plugins.qgis.org rejects __pycache__, .git, binaries).
find "$STAGE" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" -type d -name '.git' -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete 2>/dev/null || true

# 6. Zip with the plugin folder as the single top-level directory.
rm -f "$OUT"
( cd "$WORK" && zip -qr "$OUT" "$PLUGIN" )

VER="$(grep -E '^version=' "$ROOT/metadata.txt" | cut -d= -f2)"
echo "built $OUT  (version $VER)"
LISTING="$(unzip -l "$OUT")"           # capture once — avoid pipefail+grep -q SIGPIPE races
echo "top-level entries:"
echo "$LISTING" | awk 'NR>3 && $4 ~ /^MetadataManager\/[^/]+\/?$/ {print "  "$4}' | sort -u
# Fail loudly if a required subpackage or the license is missing (broken-build symptoms).
for want in db/ processors/ widgets/ LICENSE metadata.txt; do
  echo "$LISTING" | grep -q "$PLUGIN/$want" || { echo "ERROR: $want missing from zip"; exit 1; }
done
echo "OK — subpackages, LICENSE and metadata all present."
