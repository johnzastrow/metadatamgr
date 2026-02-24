"""
Pytest configuration for Metadata Manager tests.

Installs stub modules for qgis.* into sys.modules so that the test
package __init__.py (which does `import qgis`) and any unit tests that
mock QGIS classes can be collected and run outside a live QGIS environment.

Tests that exercise QGIS-dependent logic (rendering, layer loading, etc.)
still require a real QGIS instance and must be run inside QGIS.
"""

import sys
from unittest.mock import MagicMock


def _install_qgis_stubs():
    """Insert minimal stub modules for qgis.* before test collection."""
    qgis = MagicMock()
    qgis.core = MagicMock()
    qgis.gui = MagicMock()
    qgis.PyQt = MagicMock()
    qgis.PyQt.QtCore = MagicMock()
    qgis.PyQt.QtGui = MagicMock()
    qgis.PyQt.QtWidgets = MagicMock()

    sys.modules.setdefault("qgis", qgis)
    sys.modules.setdefault("qgis.core", qgis.core)
    sys.modules.setdefault("qgis.gui", qgis.gui)
    sys.modules.setdefault("qgis.PyQt", qgis.PyQt)
    sys.modules.setdefault("qgis.PyQt.QtCore", qgis.PyQt.QtCore)
    sys.modules.setdefault("qgis.PyQt.QtGui", qgis.PyQt.QtGui)
    sys.modules.setdefault("qgis.PyQt.QtWidgets", qgis.PyQt.QtWidgets)


_install_qgis_stubs()
