from os import environ, listdir, path
import json
import re
import shlex
import sys
from argparse import ArgumentParser
from rich import print, print_json, pretty, box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from art import text2art
from utlis import getCurrentVersion, getJournalPath
pretty.install()

JOURNAL_PATH = getJournalPath()

def _discover_journals(journal_path: str) -> list[str]:
    files = listdir(journal_path)
    pattern = r'^Journal\.\d{4}-\d{2}-\d{2}T\d{6}\.\d{2}\.log$'
    return sorted([name for name in files if re.fullmatch(pattern, name)], reverse=True)


def _load_entries(journal_path: str) -> list[dict]:
    entries: list[dict] = []
    journals = _discover_journals(journal_path)
    for journal in journals:
        items = []
        with open(path.join(journal_path, journal), 'r', encoding='utf-8') as file_obj:
            for line in file_obj.readlines():
                try:
                    items.append(json.loads(line))
                except json.decoder.JSONDecodeError:
                    print(journal, line)
                    continue

        for idx, item in enumerate(reversed(items), start=1):
            entries.append(
                {
                    'journal': journal,
                    'line': len(items) - idx + 1,
                    'item': item,
                }
            )
    return entries


def _normalize(value: str, case_sensitive: bool) -> str:
    return value if case_sensitive else value.casefold()


def _match_text(search_term: str, candidate_text: str, exact: bool, case_sensitive: bool) -> bool:
    search_value = _normalize(search_term, case_sensitive)
    candidate_value = _normalize(candidate_text, case_sensitive)
    if exact:
        return search_value == candidate_value
    return search_value in candidate_value


def _entry_matches(
    item: dict,
    search_event: str | None = None,
    search_word: str | None = None,
    exact: bool = False,
    case_sensitive: bool = False,
) -> bool:
    if search_event is not None and not _match_text(search_event, item.get('event', ''), exact=exact, case_sensitive=case_sensitive):
        return False

    if search_word is not None:
        if exact:
            search_parts = [str(value) for value in list(item.keys()) + list(item.values())]
            if not any(
                _match_text(search_word, part, exact=True, case_sensitive=case_sensitive)
                for part in search_parts
            ):
                return False
        else:
            searchable_payload = str(list(item.keys()) + list(item.values()))
            if not _match_text(search_word, searchable_payload, exact=False, case_sensitive=case_sensitive):
                return False

    return True


def journal_search(
    entries: list[dict],
    search_event: str | None = None,
    search_word: str | None = None,
    search_limit: int = 100,
    exact: bool = False,
    case_sensitive: bool = False,
) -> int:
    if search_event is None and search_word is None:
        raise ValueError('Please specify either an event or a word to search for.')

    found = 0
    for entry in entries:
        item = entry['item']
        if _entry_matches(
            item,
            search_event=search_event,
            search_word=search_word,
            exact=exact,
            case_sensitive=case_sensitive,
        ):
            print(f"{entry['journal']} line {entry['line']} {item.get('event', 'UnknownEvent')}")
            print_json(data=item)
            found += 1
            if found >= search_limit:
                print(f'search limit {search_limit} reached')
                return found
    return found


def journal_search_streaming(
    journal_path: str,
    search_event: str | None = None,
    search_word: str | None = None,
    search_limit: int = 100,
    exact: bool = False,
    case_sensitive: bool = False,
) -> int:
    if search_event is None and search_word is None:
        raise ValueError('Please specify either an event or a word to search for.')

    found = 0
    journals = _discover_journals(journal_path)
    for journal in journals:
        items = []
        with open(path.join(journal_path, journal), 'r', encoding='utf-8') as file_obj:
            for line in file_obj.readlines():
                try:
                    items.append(json.loads(line))
                except json.decoder.JSONDecodeError:
                    print(journal, line)
                    continue

        for idx, item in enumerate(reversed(items), start=1):
            if _entry_matches(
                item,
                search_event=search_event,
                search_word=search_word,
                exact=exact,
                case_sensitive=case_sensitive,
            ):
                line_number = len(items) - idx + 1
                print(f"{journal} line {line_number} {item.get('event', 'UnknownEvent')}")
                print_json(data=item)
                found += 1
                if found >= search_limit:
                    print(f'search limit {search_limit} reached')
                    return found
    return found


def interactive_search_loop(
    entries: list[dict],
    default_limit: int,
    default_exact: bool = False,
    default_case_sensitive: bool = False,
) -> None:
    print('[bold cyan]Interactive mode[/bold cyan] - enter search args like "-e FSDJump -w Stronghold -l 5 --exact --case-sensitive" or type "q" to quit.')

    interactive_parser = ArgumentParser(prog='interactive-search', add_help=False)
    interactive_parser.add_argument('-e', '--event', dest='event', default=None)
    interactive_parser.add_argument('-w', '--word', dest='word', default=None)
    interactive_parser.add_argument('-l', '--limit', dest='limit', default=default_limit, type=int)
    interactive_parser.add_argument('-x', '--exact', action='store_true', dest='exact', default=default_exact)
    interactive_parser.add_argument('-c', '--case-sensitive', action='store_true', dest='case_sensitive', default=default_case_sensitive)

    while True:
        raw_input = input('search> ').strip()
        if raw_input.lower() in {'q', 'quit', 'exit'}:
            print('Exiting interactive mode.')
            return

        if not raw_input:
            print('Please provide args, for example: -e FSDJump -w Stronghold -l 5')
            continue

        try:
            parsed = interactive_parser.parse_args(shlex.split(raw_input))
        except SystemExit:
            print('Invalid input. Use: -e EVENT -w WORD -l LIMIT')
            continue

        event = parsed.event
        word = parsed.word
        limit = parsed.limit
        exact = parsed.exact
        case_sensitive = parsed.case_sensitive
        if event is None and word is None:
            print('Please provide at least -e or -w.')
            continue

        print(
            f'Searching for event={event!r}, word={word!r}, '
            f'limit={limit}, exact={exact}, case_sensitive={case_sensitive}'
        )
        matches = journal_search(
            entries=entries,
            search_event=event,
            search_word=word,
            search_limit=limit,
            exact=exact,
            case_sensitive=case_sensitive,
        )
        print(f'Found {matches} matching entries.')

console = Console(log_path=False)
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-e", "--event",
                    action="store", dest="event", default=None,
                    help="journal event to search for")
    parser.add_argument("-w", "--word",
                    action="store", dest="word", default=None,
                    help="word to search for in journal entries")
    parser.add_argument("-l", "--limit",
                    action="store", dest="limit", default=100, type=int,
                    help="number of journal entries to search")
    parser.add_argument("-p", "--path",
                    action="store", dest="path", default=JOURNAL_PATH,
                    help="journal path: overrides journal path")
    parser.add_argument("-i", "--interactive",
                    action="store_true", dest="interactive", default=False,
                    help="stay open for multiple searches without re-reading journals")
    parser.add_argument("-x", "--exact",
                    action="store_true", dest="exact", default=False,
                    help="use exact matching instead of partial matching")
    parser.add_argument("-c", "--case-sensitive",
                    action="store_true", dest="case_sensitive", default=False,
                    help="use case-sensitive matching (default is case-insensitive)")
    args = parser.parse_args()
    if console.width >= 140:
        console_size = 'xlarge'
    elif console.width >= 120:
        console_size = 'large'
    elif console.width >= 80:
        console_size = 'medium'
    else:
        console_size = 'small'
    print(Panel(Align.center(Text(text2art("EDJS", f'rnd-{console_size}'))), title=f"Elite Dangerous Journal Searcher {getCurrentVersion()}", subtitle="by Skywalker-Elite", style='bold blue', expand=True, padding=1, box=box.DOUBLE))
    assert args.path is not None, "Journal path cannot be None"
    assert path.exists(args.path), f"Journal path does not exist: {args.path}"
    print(f'Using journal path: {args.path}')
    has_initial_search = bool(args.event or args.word)

    loaded_entries = None
    if args.interactive or not has_initial_search:
        print('Loading journals into memory...')
        loaded_entries = _load_entries(args.path)
        print(f'Loaded {len(loaded_entries)} entries.')

    if args.event and args.word:
        print(f'Searching for event: {args.event} and word: {args.word}')
        if args.interactive:
            journal_search(
                entries=loaded_entries,
                search_event=args.event,
                search_word=args.word,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        else:
            journal_search_streaming(
                journal_path=args.path,
                search_event=args.event,
                search_word=args.word,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        if args.interactive:
            interactive_search_loop(
                entries=loaded_entries,
                default_limit=args.limit,
                default_exact=args.exact,
                default_case_sensitive=args.case_sensitive,
            )
    elif args.event:
        print(f'Searching for event: {args.event}')
        if args.interactive:
            journal_search(
                entries=loaded_entries,
                search_event=args.event,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        else:
            journal_search_streaming(
                journal_path=args.path,
                search_event=args.event,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        if args.interactive:
            interactive_search_loop(
                entries=loaded_entries,
                default_limit=args.limit,
                default_exact=args.exact,
                default_case_sensitive=args.case_sensitive,
            )
    elif args.word:
        print(f'Searching for word: {args.word}')
        if args.interactive:
            journal_search(
                entries=loaded_entries,
                search_word=args.word,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        else:
            journal_search_streaming(
                journal_path=args.path,
                search_word=args.word,
                search_limit=args.limit,
                exact=args.exact,
                case_sensitive=args.case_sensitive,
            )
        if args.interactive:
            interactive_search_loop(
                entries=loaded_entries,
                default_limit=args.limit,
                default_exact=args.exact,
                default_case_sensitive=args.case_sensitive,
            )
    else:
        interactive_search_loop(
            entries=loaded_entries,
            default_limit=args.limit,
            default_exact=args.exact,
            default_case_sensitive=args.case_sensitive,
        )