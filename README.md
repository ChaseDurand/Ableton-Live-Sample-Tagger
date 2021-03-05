# Ableton Live Sample Tagger

"Don't delete these!"

This is a janky utility for tagging samples that appear in any Ableton Live Set to make sample library cleaning/deleting risk free. It tags samples using the red tag 0 with Live's "collection" browser feature (introduced in Live 10). This is especially useful for people like me who download too many free samples online, use a handful of them, and run out of disk space. Now you can safely delete samples without risk of unknowingly breaking projects by deleting a sample used somewhere.

This utility finds all non-backup Ableton Live Sets in a given directory, parses them to find all unique samples (Ableton Live Sets are gzipped xml files), and adds a tag via an xmp file.

Limitations (a lot):
-  I don't know python.
-  I don't know basic coding conventions.
-  Only tags samples in user-defined folders. Samples from Core Library and Packs are not included (the xmp location is different relative to the sample from user-library samples).
-  Only tested on a single computer (Live 10.1.30, macOS 10.15).
-  Only works for single volumes.
-  File paths are hard coded in (no CLI or ease of use features).


I ~~stole~~ took inspiration from a lot of elements of Elixir Beats' code: https://github.com/elixirbeats/abletoolz

I can not overstate how hacky my current implementation is, but I hope someone finds it useful.
