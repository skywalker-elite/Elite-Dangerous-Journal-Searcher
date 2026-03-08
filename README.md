# Journal Searcher

A lightweight command-line tool to search Elite Dangerous journal entries by event and/or text.

## Running the executable
Pre-built executables are available on the [Releases](https://github.com/skywalker-elite/Elite-Dangerous-Journal-Searcher/releases) page.

To run the executable, simply download the appropriate version for your operating system, and run the `EDJS` executable. The rest of the usage is the same as running from source, just replace `uv run main.py` with `./EDJS` (Linux/Mac) or `EDJS.exe` (Windows). You can also just double-click the executable to start in interactive mode.

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

The script can be run in two modes: one-off CLI mode for quick searches, and interactive multi-search mode for more extensive exploration.
### One-off CLI mode
Run a single search directly from the command line. The script will load and parse journal files each time you run it, so this is best for quick, infrequent searches.
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

### Interactive multi-search mode

Loads and parses journal files once, keeps them in memory, and lets you run multiple searches without re-reading files. 

- Start interactive mode directly:
	- `uv run main.py` or `uv run main.py -i`
- Run one initial search, then remain interactive:
	- `uv run main.py -w Stronghold -i`

In interactive mode, type `q`, `quit`, or `exit` at a prompt to close the tool.
Use the same flags as CLI per query, for example:

- `-e FSDJump -w Stronghold -l 5`
- `-w Stronghold -l 10`
- `-w "federal dropship" -l 5`
- `-e FSDJump --exact`
- `-w Stronghold --case-sensitive`
- `-e FSDJump -x`
- `-w Stronghold -c`

Quoted phrases are supported in both one-off CLI mode and interactive mode.

Matching defaults:
- Partial matching (not exact)
- Case-insensitive matching

Arguments:
- `-e` / `--event` to specify the event type to search for
- `-w` / `--word` to specify the word or phrase to search for in the journal entries
- `-l` / `--limit` to specify the maximum number of results to display (default is 100)

Optional flags:
- `--exact` / `-x` for exact matches
- `--case-sensitive` / `-c` for case-sensitive matches
