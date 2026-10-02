# Security Policy

## Supported versions

Security fixes are applied to the latest released version. Older versions are not maintained.

## Reporting a vulnerability

Please report suspected vulnerabilities privately rather than opening a public issue:

- Preferred: GitHub's **[Report a vulnerability](../../security/advisories/new)**
  (repository **Security** tab > **Advisories**), or
- Email the maintainer at `johnzastrow@users.noreply.github.com`.

Please include steps to reproduce and the affected version. You will receive an acknowledgement
within a few days. We ask that you allow a reasonable window to release a fix before public
disclosure.

## Scope

Metadata Manager is a QGIS plugin for creating and managing layer/dataset metadata: it scans data
inventories, reads and writes metadata (into GeoPackage/SpatiaLite databases and `.qmd` sidecar
files), and parses metadata from local sources (FGDC, ESRI, ISO 19115, embedded). Relevant concerns
include local file-path handling, SQL identifier handling for the inventory/metadata databases, and
parsing of local metadata/XML documents. The plugin does not handle authentication or store
credentials.
