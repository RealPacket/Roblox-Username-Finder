# About this file:
# Allows you to log custom colored messages,
# And stops the normal messages from coming.
# From the Roblox Username Checker script.
import logging
import coloredlogs
import os
import inspect
from pathlib import Path as P
if __name__ == '__main__':
    raise Exception("Ben says \"No\".")


def get_importing_file():
    file_path = inspect.stack()[1].filename
    return os.path.basename(file_path).split(".")[0]


FolderName: str = "Twitch MultiTool"
Folder: P = P(f"{P.cwd()}\\{FolderName}")
if not Folder.exists():
    Folder.mkdir()

logger = logging.getLogger(f"{get_importing_file() or ''}")
coloredlogs.install(level="DEBUG", logger=logger,
                    fmt=f"[%(name)s | %(levelname)s | %(asctime)s] %(message)s",
                    datefmt="%I:%M %p",
                    level_styles={
                        "debug":
                            {
                                "color": "green"
                            },
                        "info":
                            {
                                "color": "blue"
                            },
                        "warning":
                            {
                                "color": "yellow"
                            },
                        "error":
                            {
                                "color": "red"
                            }
                    })

fh = logging.FileHandler(f"{FolderName}\\Log.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(f"[%(levelname)s | {get_importing_file()} | %(asctime)s] %(message)s",
                              datefmt="%I:%M")
fh.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)


def err(msg: str):
    logger.error(msg)


def warn(msg: str):
    logger.warning(msg)


def debug(msg: str):
    logger.debug(msg)


def log(level: int, msg: str):
    logger.log(level, msg)


def info(msg: str):
    logger.info(msg)
