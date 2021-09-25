import unittest
from pathlib import Path
from unittest.case import expectedFailure
from src.als import *
from testResources import *


class testals(unittest.TestCase):
    def test_getALSFiles(self):
        self.assertIn(Path('Tests/testSet Project/testSet.als'),
                      getALSFiles(Path()))
        self.assertIn(Path('Tests/testSet Project/testSet2.als'),
                      getALSFiles(Path()))
        # Check if files can be found in nested folders
        self.assertIn(Path('Tests/testSet Project/testFolder/testSet3.als'),
                      getALSFiles(Path()))
        # Check if files can be found in nested folders
        self.assertIn(
            Path('Tests/testSet Project/testFolder/testFolder2/testSet4.als'),
            getALSFiles(Path()))
        # Check if backups are ignored
        self.assertNotIn(
            Path('Tests/testSet Project/testSet [2021-09-24 232020].als'),
            getALSFiles(Path()))