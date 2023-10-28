import os
import asyncio
from typing import Tuple, Dict
import queue
import argparse

FILE_INFO = {
    "path": "",  
    "name": "",  
    "size": 0    
}

EOD = {"status": "end_of_directory"}
ASYNC_INTERRUPT = {"status": "interrupted"}

async def search_by_filename(filename: str) -> Tuple[queue.Queue, Dict]:
    q = queue.Queue()
    interrupt = ASYNC_INTERRUPT
    visited_paths = set()

    async def async_readdir(path: str, depth=0):
        if depth > 10:
            return

        if path in visited_paths:
            return

        visited_paths.add(path)

        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file() and entry.name == filename:
                        file_info = {
                            "path": entry.path,
                            "name": entry.name,
                            "size": entry.stat().st_size
                        }
                        print(f"Found: {file_info['path']}")  # This line will print the found file path immediately
                        q.put(file_info)
                    elif entry.is_dir():
                        await async_readdir(entry.path, depth+1)
        except PermissionError:
            pass

    await async_readdir('C:/')
    q.put(EOD)
    return q, interrupt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for files by filename across the entire system")
    parser.add_argument('filename', type=str, help='Filename to search for')

    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    q, interrupt = loop.run_until_complete(search_by_filename(args.filename))
    
    while not q.empty():
        print(q.get())
