import date_pin
import guess_ext
from queue import Queue
from datetime import datetime

class FrontAPI:
    @classmethod
    def security_check():
        pass

    @classmethod
    def check_unmatched_ext(cls, fileinfo:dict)->bool:
        guess_ext.guess_ext(fileinfo)
    
    @classmethod
    def get_fileinfo_in_directory(cls, directory:str):
        q = Queue()
        q.put({
            "path" : directory,
            "filename" : "test1.exe",
            "ext" : "exe",
            "date_lastchanged" : datetime(2022,10,2, 12,30,4),
            "date_lastaccess" : datetime(2022,10,2, 14,12,10),
            "date_create" : datetime(2022,10,2, 12,30,4),
            "addition" : {},
            "eod" : False
        })
        q.put({
            "path" : directory,
            "filename" : "test2.txt",
            "ext" : "txt",
            "date_lastchanged" : datetime(2022,10,4, 12,30,4),
            "date_lastaccess" : datetime(2022,10,4, 12,30,4),
            "date_create" : datetime(2022,10,3, 3,3,20),
            "addition" : {},
            "eod" : False
        })
        q.put({
            "eod" : True
        })
        return q
    
    @classmethod
    def get_fileinfo(cls):
        pass

    def search_files(cls, directory:str, filefilters:dict):
        q = Queue()
        q.put({
            "path" : directory,
            "filename" : "searchresult.txt",
            "ext" : "txt",
            "date_lastchanged" : datetime(2022,10,4, 12,30,4),
            "date_lastaccess" : datetime(2022,10,4, 12,30,4),
            "date_create" : datetime(2022,10,3, 3,3,20),
            "addition" : {},
            "eod" : False
        })
        q.put({
            "eod" : True
        })

        return q