import filter as Filter
import datetime
from config import Config

LOGGING_SETTINGS = Config().get()["settings"]["logging"]
USE_SESSION_LOG_FILE = LOGGING_SETTINGS["use_session_log_file"]
SESSION_LOG_FILENAME = LOGGING_SETTINGS["session_log_filename"]
SESSION_BUFFER_NAME = LOGGING_SETTINGS["session_buffer_name"]

if USE_SESSION_LOG_FILE:
    LOG_FILE_HANDLE = open(SESSION_LOG_FILENAME, "w+")

def write_to_log(log_string):
    if USE_SESSION_LOG_FILE:
        LOG_FILE_HANDLE.write(log_string)
    log_lines = Filter.call_filter_class(log_string, SESSION_BUFFER_NAME)
    full_cache = Config().get()["internal"]["buffer_caches"][SESSION_BUFFER_NAME]
    if Config().get()["settings"]["logging"]["add_timestamp"]:
        full_cache.append("--- {0} ---".format(datetime.datetime.utcnow()))
    full_cache.extend(log_lines)
    Config().get()["internal"]["buffer_caches"][SESSION_BUFFER_NAME] = full_cache
