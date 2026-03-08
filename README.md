# Journal Searcher

A lightweight tool to search Elite Dangerous journal entries by event and/or text.

## Running from source
Prerequisites:

Python 3.12 or later, and [uv](https://docs.astral.sh/uv/guides/install-python/) for dependency management.
1. Clone the repository:
   ```bash
   git clone https://github.com/skywalker-elite/Elite-Dangerous-Journal-Searcher.git
   cd Elite-Dangerous-Journal-Searcher
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

And you're ready to run the script!

## Usage

- One-off search by word:
	- `uv run main.py -w Stronghold -l 50`
- One-off search by event:
	- `uv run main.py -e FSDJump -l 25`
- Search by both event and word:
	- `uv run main.py -e FSDJump -w Stronghold -l 25`
- Exact matching:
	- `uv run main.py -e FSDJump --exact`
	- `uv run main.py -e FSDJump -x`
- Case-sensitive matching:
	- `uv run main.py -w Stronghold --case-sensitive`
	- `uv run main.py -w Stronghold -c`

## Interactive multi-search mode

The script now loads and parses journal files once, keeps them in memory, and lets you run multiple searches without re-reading files.

- Start interactive mode directly:
	- `uv run main.py`
- Run one initial search, then remain interactive:
	- `uv run main.py -w Stronghold -i`

In interactive mode, type `q`, `quit`, or `exit` at a prompt to close the tool.
Use the same flags as CLI per query, for example:

- `-e FSDJump -w Stronghold -l 5`
- `-w Stronghold -l 10`
- `-w "federal station" -l 5`
- `-e FSDJump --exact`
- `-w Stronghold --case-sensitive`
- `-e FSDJump -x`
- `-w Stronghold -c`

Quoted phrases are supported in both one-off CLI mode and interactive mode.

Matching defaults:
- Partial matching (not exact)
- Case-insensitive matching

Optional flags:
- `--exact` / `-x` for exact matches
- `--case-sensitive` / `-c` for case-sensitive matches
