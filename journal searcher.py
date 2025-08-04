from os import listdir, path, environ
import re
import json
from argparse import ArgumentParser
user_path = environ.get('USERPROFILE')
JOURNAL_PATH = path.join(user_path, 'Saved Games', 'Frontier Developments', 'Elite Dangerous') if user_path else '.'

def journal_search(search_event:str|None=None, search_word:str|None=None, search_limit=100, journal_path=JOURNAL_PATH):
    assert (search_event is not None) or (search_word is not None)
    n_found = 0
    files = listdir(journal_path)
    r = r'^Journal\.\d{4}-\d{2}-\d{2}T\d{6}\.\d{2}\.log$'
    journals = sorted([i for i in files if re.fullmatch(r, i)], reverse=True)
    for journal in journals:
        with open(path.join(journal_path, journal), 'r', encoding='utf-8') as f:
            items = []
            for i in f.readlines():
                try:
                    items.append(json.loads(i))
                except json.decoder.JSONDecodeError: # ignore ill-formated entries
                    print(journal, i)
                    continue
        if search_event != None and search_word != None:
            for i, item in enumerate(reversed(items)):
                if search_event in item['event'] and search_word in str(list(item.keys()) + list(item.values())):
                    print(f'{journal} line {len(items) - i} {item['event']}')
                    # print(*item.items())
                    print(json.dumps(item))
                    n_found += 1
                    if n_found >= search_limit:
                        print(f'search limit {search_limit} reached')
                        return
            continue
                    
        elif search_event != None and search_word == None:
            for i, item in enumerate(reversed(items)):
                if search_event in item['event']:
                    print(f'{journal} line {len(items) - i} {item['event']}')
                    # print(*item.items())
                    print(json.dumps(item))
                    n_found += 1
                    if n_found >= search_limit:
                        print(f'search limit {search_limit} reached')
                        return
            continue
                
        elif search_word != None and search_event == None:
            for i, item in enumerate(reversed(items)):
                if search_word in str(list(item.keys()) + list(item.values())):
                    print(f'{journal} line {len(items) - i} {item['event']}')
                    # print(*item.items())
                    print(json.dumps(item))
                    n_found += 1
                    if n_found >= search_limit:
                        print(f'search limit {search_limit} reached')
                        return
            continue

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
    args = parser.parse_args()
    print(f'Using journal path: {args.path}')
    if args.event and args.word:
        print(f'Searching for event: {args.event} and word: {args.word}')
        journal_search(search_event=args.event, search_word=args.word, search_limit=args.limit, journal_path=args.path)
    elif args.event:
        print(f'Searching for event: {args.event}')
        journal_search(search_event=args.event, search_limit=args.limit, journal_path=args.path)
    elif args.word:
        print(f'Searching for word: {args.word}')
        journal_search(search_word=args.word, search_limit=args.limit, journal_path=args.path)
    else:
        raise ValueError('Please specify either an event or a word to search for.')