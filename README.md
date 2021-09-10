# Ableton Live Sample Tagger

"Don't delete these!"

This is a utility for tagging samples that appear across any Ableton Live Set to make sample library cleaning/deleting risk free. It tags samples using the red tag 0 with Live's "collection" browser feature (introduced in Live 10) and logs samples in a SQLite database. This is especially useful for people like me who download too many free samples online, use a handful of them, and run out of disk space. Now you can safely delete samples via Live's browser without the risk of unknowingly breaking projects by deleting samples they use.

This utility finds all non-backup Ableton Live Sets in a given directory, parses them to find all unique samples (Ableton Live Sets are gzipped xml files), and adds a tag via an xmp file (used by Live for collection tags).

Scripts in the [Analysis](/Analysis) folder provide basic data summaries/highlights.

Tested on Live 10, macOS (10.13 and 10.15).

## Usage

Run [main.py](/main.py) from any location, then enter the root directory of project files when prompted.

## Disclaimer

_This project is not endorsed or affaliated with Ableton in any way. "Ableton" is a trademark of Ableton AG._
