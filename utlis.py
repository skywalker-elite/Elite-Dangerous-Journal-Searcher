import os
import sys

def getResourcePath(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def getCurrentVersion() -> str:
    with open(getResourcePath('VERSION'), 'r') as f:
        return f.readline().strip()
    
def getJournalPath() -> str|None:
    if sys.platform == 'win32':
        user_path = os.environ.get('USERPROFILE')
        return os.path.join(user_path, 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
    elif sys.platform == 'linux':
        user_path = os.path.expanduser('~')
        return os.path.join(user_path, '.local', 'share', 'Steam', 'steamapps', 'compatdata', '359320', 'pfx', 'drive_c', 'users', 'steamuser', 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
    else:
        return None