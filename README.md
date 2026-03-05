# Journal Searcher

Search Elite Dangerous journal entries by event and/or text.

## Usage

- One-off search by word:
	- `uv run ".\\journal searcher.py" -w Stronghold -l 50`
- One-off search by event:
	- `uv run ".\\journal searcher.py" -e FSDJump -l 25`
- Search by both event and word:
	- `uv run ".\\journal searcher.py" -e FSDJump -w Stronghold -l 25`
- Exact matching:
	- `uv run ".\\journal searcher.py" -e FSDJump --exact`
	- `uv run ".\\journal searcher.py" -e FSDJump -x`
- Case-sensitive matching:
	- `uv run ".\\journal searcher.py" -w Stronghold --case-sensitive`
	- `uv run ".\\journal searcher.py" -w Stronghold -c`

## Interactive multi-search mode

The script now loads and parses journal files once, keeps them in memory, and lets you run multiple searches without re-reading files.

- Start interactive mode directly:
	- `uv run ".\\journal searcher.py"`
- Run one initial search, then remain interactive:
	- `uv run ".\\journal searcher.py" -w Stronghold -i`

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
