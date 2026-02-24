import sys
import unittest

# conftest.py has already installed _AutoMockModule stubs for qgis.* into
# sys.modules before pytest collects this file.  We retrieve those stubs and
# pin the specific attributes that inventory_processor.py reads so that the
# field-creation logic is exercised correctly.  We do NOT replace the stubs
# with bare types.ModuleType objects; doing so would remove the __getattr__
# fallback that lets transitive imports (e.g. inventory_runner.py) resolve
# names like QObject and pyqtSignal without errors.

# ── Retrieve existing stubs ───────────────────────────────────────────────
qgis_core = sys.modules['qgis.core']
qgis_PyQt_QtCore = sys.modules['qgis.PyQt.QtCore']


# ── Concrete classes needed by InventoryProcessor ────────────────────────
class QVariant:
    String = 1
    Int = 2
    LongLong = 3
    Double = 4
    Bool = 5


class QgsField:
    def __init__(self, name, type_val=None):
        self._name = name
        self._type_val = type_val

    def name(self):
        return self._name


class QgsFields(list):
    def append(self, f):
        super().append(f)

    def toList(self):
        return list(self)


# ── Pin attributes on the existing stubs ─────────────────────────────────
qgis_core.QgsField = QgsField
qgis_core.QgsFields = QgsFields
# Remaining qgis.core names (QgsVectorLayer, etc.) are handled by __getattr__

qgis_PyQt_QtCore.QVariant = QVariant
# QObject, pyqtSignal, QThread, etc. are handled by __getattr__


# ── Import the class under test ───────────────────────────────────────────
from processors.inventory_processor import InventoryProcessor


class TestInventoryProcessorFields(unittest.TestCase):
    def test_create_fields_count_and_names(self):
        params = {
            'directory': '.',
            'output_gpkg': 'out.gpkg',
            'layer_name': 'inv',
            'update_mode': False,
            'include_vectors': True,
            'include_rasters': True,
            'include_tables': True,
            'parse_metadata': False,
            'include_sidecar': False,
            'validate_files': False,
        }
        proc = InventoryProcessor(params, feedback=None)
        fields = proc._create_fields()
        self.assertTrue(hasattr(fields, 'toList') or isinstance(fields, list))
        self.assertGreater(len(fields), 40)
        names = [f.name() for f in fields]
        for key in ('file_path', 'layer_name', 'data_type',
                    'file_size_bytes', 'metadata_status'):
            self.assertIn(key, names)


if __name__ == '__main__':
    unittest.main()
