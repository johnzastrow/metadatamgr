"""
Pytest configuration for Metadata Manager tests.

Installs stub modules for qgis.* into sys.modules so that the test
package __init__.py (which does `import qgis`) and any unit tests can
be collected and run outside a live QGIS environment.

Uses types.ModuleType subclasses with __getattr__ so that both attribute
access (qgis.core.QgsField) and explicit imports
(from qgis.PyQt.QtCore import QObject) return MagicMock objects.

Tests that exercise QGIS-dependent logic (rendering, layer loading, etc.)
still require a real QGIS instance and must be run inside QGIS.
"""

import sys
import types
from unittest.mock import MagicMock


def _install_qgis_stubs():
    """Insert stub modules for qgis.* before test collection."""

    class _AutoMockModule(types.ModuleType):
        """Module subclass that returns a MagicMock for any unknown attribute.
        Supports both `import qgis.core; qgis.core.Foo` and
        `from qgis.PyQt.QtCore import QObject` import styles.
        """
        def __getattr__(self, name: str):
            mock = MagicMock(name=f"{self.__name__}.{name}")
            setattr(self, name, mock)
            return mock

    for mod_name in [
        "qgis",
        "qgis.core",
        "qgis.gui",
        "qgis.PyQt",
        "qgis.PyQt.QtCore",
        "qgis.PyQt.QtGui",
        "qgis.PyQt.QtWidgets",
        # GDAL Python bindings (osgeo) used by inventory_processor.py
        "osgeo",
        "osgeo.gdal",
        "osgeo.ogr",
    ]:
        sys.modules.setdefault(mod_name, _AutoMockModule(mod_name))


_install_qgis_stubs()
