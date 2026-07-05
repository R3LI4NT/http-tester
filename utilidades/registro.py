import logging
from colorama import Fore, Style

class ColoresFormatter(logging.Formatter):
    def format(self, record):
        if record.levelname == "INFO":
            record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
        elif record.levelname == "WARNING":
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelname == "ERROR":
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        elif record.levelname == "DEBUG":
            record.msg = f"{Fore.CYAN}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

_logger_configurado = False

def configurar_registro():
    global _logger_configurado
    
    logger = logging.getLogger("DOS")
    
    if not _logger_configurado:
        logger.setLevel(logging.INFO)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        handler = logging.StreamHandler()
        handler.setFormatter(ColoresFormatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        
        logger.addHandler(handler)
        _logger_configurado = True
        
    return logger