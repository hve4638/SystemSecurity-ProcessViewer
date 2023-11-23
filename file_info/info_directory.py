import os
import asyncio
import queue
from typing import Tuple, Dict
from file_info import info_file

ASYNC_INTERRUPT = {"interrupt": False}

def sync_scandir(dir_path):
    return list(os.scandir(dir_path))

async def explore_directory(dir_path, result_queue, interrupt_flag):
    try:
        files = await asyncio.to_thread(sync_scandir, dir_path)
        for file in files:
            if interrupt_flag.is_set():
                return
            
            if file.is_file():
                file_info = info_file(file.path)
                result_queue.put(file_info)
            
            elif file.is_dir():
                await explore_directory(file.path, result_queue, interrupt_flag)
   
    except (PermissionError, FileNotFoundError) as e:
        result_queue.put({"error": str(e)})

                         
async def info_directory(directory: str) -> Tuple[queue.Queue, dict]:
    result_queue = queue.Queue()
    interrupt_flag = asyncio.Event()

    try:
        await explore_directory(directory, result_queue, interrupt_flag)
 
    except (PermissionError, FileNotFoundError) as e:
        result_queue.put({"error": str(e)})

    finally:
        interrupt_flag.set()

    return result_queue, ASYNC_INTERRUPT
