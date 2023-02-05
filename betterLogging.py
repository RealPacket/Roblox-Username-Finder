# About this file:
# Allows you to log custom colored messages,
# And stops the normal messages from coming.
import sys
import logging
import coloredlogs
import os
import inspect


def get_importing_file():
    file_path = inspect.stack()[1].filename
    return os.path.basename(file_path).split(".")[0]


class CustomOutHandler:
    def write(self, message):
        if message != "":
            original_stdout.write(message)
            self.useless()

    def flush(self):
        self.useless()
        return original_stdout.flush()

    def useless(self):
        pass


class CustomErrHandler:
    def write(self, message) -> int:  # NOQA
        if message != "":
            return original_stderr.write(message)

    def flush(self) -> None:  # NOQA
        return original_stderr.flush()


original_stdout = sys.stdout
original_stderr = sys.stderr

sys.stdout = CustomOutHandler()
sys.stderr = CustomErrHandler()

logger = logging.getLogger(f"{get_importing_file() or ''}")
coloredlogs.install(level="DEBUG", logger=logger,
                    fmt=f"[%(name)s | %(levelname)s | %(asctime)s] %(message)s",
                    datefmt="%I:%M",
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

fh = logging.FileHandler("Roblox Username Scanner\\Log.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(f"[%(levelname)s : {get_importing_file()} | %(asctime)s] %(message)s",
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
