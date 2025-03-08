from os import listdir, path, environ
import re
import json
user_path = environ.get('USERPROFILE')
JOURNAL_PATH = path.join(user_path, 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
search_limit = 500

def journal_search(search_event=None, search_word=None):
    assert (search_event is not None) ^ (search_word is not None)
    n_found = 0
    files = listdir(JOURNAL_PATH)
    r = r'^Journal\.\d{4}-\d{2}-\d{2}T\d{6}\.\d{2}\.log$'
    journals = sorted([i for i in files if re.fullmatch(r, i)], reverse=True)
    for journal in journals:
        with open(path.join(JOURNAL_PATH, journal), 'r', encoding='utf-8') as f:
            items = []
            for i in f.readlines():
                try:
                    items.append(json.loads(i))
                except json.decoder.JSONDecodeError: # ignore ill-formated entries
                    print(journal, i)
                    continue
            for i, item in enumerate(reversed(items)): # Parse from new to old
                if search_event and search_event in item['event']:
                    print(f'{journal} line {i+1} {item['event']}')# {item}')
                    n_found += 1
                if search_word and search_word in str(list(item.keys()) + list(item.values())):
                    print(f'{journal} line {i+1} {item['event']}')# {item}')
                    n_found += 1
                if n_found >= search_limit:
                    print(f'search limit {search_limit} reached')
                    break
        if n_found >= search_limit:
            print(f'search limit {search_limit} reached')
            break

if __name__ == '__main__':
    # journal_search(search_word='3702539520')
    # journal_search(search_event='CarrierJumpRequest')
    # journal_search(search_word='Rudolph Enterprise')
    journal_search(search_word='HIP 78825')