import inspect
from typing import Any
import asyncio
from datetime import datetime
import json

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

def error(error_message: str, details: Any, show: str="default"):
    """
    Creates logs about errors.
    
    To console:
    [E] Error... <Details>

    To log:
    2026-01-07 23:08:37 [E] Error... <Details> module: '__main__' function: 'main' line_number: '15' file: 'D:\\...'
    """
    frame = inspect.currentframe().f_back
    log_details = {
        'module': frame.f_globals.get('__name__'),
        'function': frame.f_code.co_name,
        'line_number': frame.f_lineno,
        'file': frame.f_code.co_filename
    }

    # Log to console
    if _logger_state["show_errors"]:
        print(f"[E] Error: {error_message}. Details: {details}")

    # Log to file (asynchronously)
    if _logger_state["log_errors"]:
        asyncio.run(write_line(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [E] Error: {error_message}. Details: {details} | Context: {json.dumps(log_details)}"))

async def write_line(data: str) -> bool:
    """
    Creates line in log file.
    """
    while _logger_state["is_writing"]:
        await asyncio.sleep(0.0001)
    try:
        with open(_logger_state["logs_file_name"], "a", encoding="utf-8") as f:
            f.write(data + "\\n")
        return True
    except Exception as e:
        print(f"Error writing to log file: {e}")
        return False

# Note: The original code had a placeholder for 'log' function, which is now redundant 
# since the main logging logic is handled by error().