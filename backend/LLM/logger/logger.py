import inspect
from datetime import datetime
import json
import os

_logger_state = {
    "show_info": True,
    "show_errors": True,
    "log_info": True,
    "log_errors": True,
    "logs_file_name": "work_info.log"
}

def _write_line(data: str) -> None:
    try:
        with open(_logger_state["logs_file_name"], "a", encoding="utf-8") as f:
            f.write(data + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def log(message: str, level: str = "INFO") -> None:
    """Логирование информационных сообщений."""
    frame = inspect.currentframe().f_back
    log_details = {
        'module': frame.f_globals.get('__name__'),
        'function': frame.f_code.co_name,
        'line_number': frame.f_lineno,
        'file': frame.f_code.co_filename
    }
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} [{level}] {message} | Context: {json.dumps(log_details)}"
    
    if _logger_state["show_info"] and level == "INFO":
        print(f"[I] {message}")
    if _logger_state["show_errors"] and level == "ERROR":
        print(f"[E] {message}")
    
    if (level == "INFO" and _logger_state["log_info"]) or (level == "ERROR" and _logger_state["log_errors"]):
        _write_line(log_line)

def error(error_message: str, details: any = None, show: str = "default"):
    """Логирование ошибок."""
    msg = f"{error_message}" + (f" Details: {details}" if details else "")
    log(msg, "ERROR")