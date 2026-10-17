import time
import os
import ConfigReader
peers = ConfigReader.read_peer_info()
logStarted = False
from datetime import datetime, timezone, timedelta
from pathlib import Path

def ensure_file_exists(filename: str):
    file_path = Path(filename)
    if file_path.is_file():
        pass
    else:
        file_path.touch()
        print(f"'{filename}' did not exist and has been created.")
