import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


class App_Logger:

    log_formatter = logging.Formatter(f"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line %(lineno)d) - %(message)s",
                datefmt="%d-%m-%Y %H:%M:%S")

    def __init__(self):
        pass

    def get_file_handler(self) -> logging.FileHandler :
        # create logs folder if it doesn't exist
        Path("../logs").mkdir(parents=True, exist_ok=True)
        file_handler = TimedRotatingFileHandler(f"../logs/app.log", when='d')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(App_Logger.log_formatter)
        return file_handler

    def get_stream_handler(self) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(App_Logger.log_formatter)
        return stream_handler

    def get_logger(self, name) -> logging.Logger:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.get_file_handler())
        self.logger.addHandler(self.get_stream_handler())
        return self.logger