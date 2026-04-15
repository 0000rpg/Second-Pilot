import inspect
from typing import Any
import asyncio
from datetime import datetime

_logger_state = {
    "show_info": False,
    "show_errors": True,
    "log_info": True,
    "log_errors": True,
    "logs_file_name": "work_info.log",
    "is_writing": False
}

def log():
    """
    Generate log output to console and file.
    
    To console:
    [L] Info...

    To log:
    2026-01-07 23:08:37 [L] Info... module: '__main__' function: 'main' line_number: '15' file: 'D:\\...'
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def error(error: str, details: Any, show: str="default"):
    """
    Creates logs about errors

    To console:
    [E] Error... <Details>

    To log:
    2026-01-07 23:08:37 [E] Error... <Details> module: '__main__' function: 'main' line_number: '15' file: 'D:\\...'
    """
    
    frame = inspect.currentframe().f_back
    '''TODO {
        'module': frame.f_globals.get('__name__'),
        'function': frame.f_code.co_name,
        'line_number': frame.f_lineno,
        'file': frame.f_code.co_filename
    }'''

async def write_line(data: str) -> bool:
    """
    Creates line in log file
    """
    while _logger_state["is_writing"]:
        asyncio.sleep(0.0001)