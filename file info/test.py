import asyncio
from pprint import pprint
from info_directory import info_directory
from file_info import info_file

async def main(directory_to_scan):
    result_queue, async_interrupt = await info_directory(directory_to_scan)
    
    # 결과 큐에서 결과를 추출하고 출력합니다.
    while not result_queue.empty():
        result = result_queue.get()
        pprint(result)
        print("-----------------------------------------------------------------------------------")

if __name__ == "__main__":
    directory_to_scan = "/home/hojun/Desktop"  # 원하는 디렉토리 경로로 변경하세요.
    asyncio.run(main(directory_to_scan))
