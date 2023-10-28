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

async def search_files(directory: str, filters: Dict) -> Tuple[queue.Queue, Dict]:
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
                    if entry.is_file() and entry.name.endswith(tuple(filters.values())):
                        q.put({
                            "path": entry.path,
                            "name": entry.name,
                            "size": entry.stat().st_size
                        })
                    elif entry.is_dir():
                        await async_readdir(entry.path, depth+1)
        except PermissionError:
            pass

    await async_readdir(directory)
    
    q.put(EOD)

    return q, interrupt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for files by filters in the specified directory")
    parser.add_argument('directory', type=str, help='Starting directory for search')
    parser.add_argument('--filters', nargs='*', default=[], help='File extensions to search for, e.g. .txt .jpg')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    q, interrupt = loop.run_until_complete(search_files(args.directory, {i: f for i, f in enumerate(args.filters)}))
    while not q.empty():
        print(q.get())
