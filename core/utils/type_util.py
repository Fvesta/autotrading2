from core.logger import logger


def intOrZero(val):
    try:
        val = int(val)
    except ValueError:
        if val != '':
            logger.warning("ValueError: value can't transfer to integer")
        
        val = 0
    except TypeError:
        if val != '':
            logger.warning("TypeError: value is not correct type")
        
        val = 0
    
    return val