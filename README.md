# Ableton Live Sample Tagger

"Don't delete these!"

This is a utility for tagging samples that appear across any Ableton Live Set to make sample library cleaning/deleting risk free. It tags samples using the red tag 0 with Live's "collection" browser feature (introduced in Live 10) and logs samples in a SQLite database. This is especially useful for people like me who download too many free samples online, use a handful of them, and run out of disk space. Now you can safely delete samples via Live's browser without the risk of unknowingly breaking projects by deleting samples they use.

This utility finds all non-backup Ableton Live Sets in a given directory, parses them to find all unique samples (Ableton Live Sets are gzipped xml files), and adds a tag via an xmp file (used by Live for collection tags). On the initial run, a SQLite database is created in the provided project root folder to log all projects and samples. On later executions, projects that have been modified are scanned and new samples are added and tagged.

Limitations:
-  Only tags samples in user-defined folders. Samples from Core Library and Packs are not included (the xmp location is different relative to the sample from user-library samples).
-  Tested on Live 10.1.30, macOS 10.13 and 10.15.
-  Only works for single volumes/drives.
