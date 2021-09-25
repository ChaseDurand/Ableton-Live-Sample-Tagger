import unittest
from pathlib import Path
from unittest.case import expectedFailure
from src.xml import *
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
        self.assertFalse(checkDataBlobSize(bytearray.fromhex(hexInput3[0])))

    def test_getRelativePath(self):
        relativeFileRefs = getRelativeFileRefs()
        alsFile = Path('Tests')
        self.assertEqual(
            getRelativePath(relativeFileRefs[0], alsFile),
            Path(
                '/Users/chasedurand/Dev/Ableton-Live-Sample-Tagger/Samples/Processed/Freeze/Freeze 5-snare 2 [2021-09-24 231810].wav'
            ))

    def test_geAbsolutePath(self):
        absoluteFileRefs = getAbsoluteFileRefs()
        self.assertEqual(getAbsolutePath(absoluteFileRefs[0]),
                         Path('/Users/chasedurand/testFolder/kick.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[1]),
                         Path('/Users/chasedurand/testFolder/snare.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[2]),
                         Path('/Users/chasedurand/testFolder/kick 2.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[3]),
                         Path('/Users/chasedurand/testFolder/snare 2.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[4]),
                         Path('/Users/chasedurand/testFolder/snare 2.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[5]),
                         Path('/Users/chasedurand/testFolder/kick 3.wav'))
        self.assertEqual(getAbsolutePath(absoluteFileRefs[6]),
                         Path('/Users/chasedurand/testFolder/snare 3.wav'))