import unittest
from pathlib import Path
from unittest.case import expectedFailure
from ALST.xml import *
from testResources import *


class testxml(unittest.TestCase):
    def test_hex2path(self):
        self.assertEqual(hex2path(hexInput1[0]), Path(hexInput1[1]))
        with self.assertRaises(SystemExit) as cm:
            hex2path(hexInput2[0])
        self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            hex2path(hexInput3[0])
        self.assertEqual(cm.exception.code, 1)

    def test_checkDataBlobSize(self):
        self.assertTrue(checkDataBlobSize(bytearray.fromhex(hexInput1[0])))
        self.assertFalse(checkDataBlobSize(bytearray.fromhex(hexInput2[0])))
        self.assertFalse(checkDataBlobSize(bytearray.fromhex(hexInput2[0])))