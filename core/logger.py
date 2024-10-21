import logging
import logging.config

class Logger:
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        "formatters": {
            "basic": {
                "format": "%(asctime)s:%(levelname)s>  %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'basic',
            },
            'file_debug': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'basic',
                'filename': 'log/debug.log',
                'encoding': 'utf-8',
                'mode': 'w',
            },
            'file_error': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'basic',
                'filename': 'log/error.log',
                'encoding': 'utf-8',
                'mode': 'w',
            }
        },
        'loggers': {
            'ui': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        },
        'root': {
            'handlers': ['console', 'file_debug', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Logger, cls).__new__(cls)
        
        return cls.instance
    
    def __init__(self, level):
        if hasattr(self, "initialized"):
            return
        
        logging.config.dictConfig(self.logging_config)
        
        level_mapping = {
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'warning': logging.WARNING,
            'critical': logging.CRITICAL,
            'error': logging.ERROR
        }
        
        self.base_logger = logging.getLogger()
        self.base_logger.setLevel(level_mapping.get(level, logging.DEBUG))
        
        self.scheduler_logger = logging.getLogger("apscheduler")
        self.scheduler_logger.setLevel(level_mapping.get("warning"))

        self.initialized = True
        
    # console, file debug, file error
    def debug(self, message):
        self.base_logger.debug(message)
        
    def warning(self, message):
        self.base_logger.warning(message)
        
    # file debug, file error
    def info(self, message):
        self.base_logger.info(message)
        
    def error(self, message):
        self.base_logger.error(message)
        
    def debugSessionStart(self, message="함수실행"):
        self.base_logger.debug("")
        self.base_logger.debug(f"start < {f' {message} ':ㅡ^30}")
        
    def debugSessionFin(self, message="함수종료"):
        self.base_logger.debug(f"{f' {message} ':ㅡ^30} > end")
        self.base_logger.debug("")
        
logger = Logger("debug")
    