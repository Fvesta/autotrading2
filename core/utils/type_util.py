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

def absIntOrZero(val):
    try:
        val = abs(int(val))
    except ValueError:
        if val != '':
            logger.warning("ValueError: value can't transfer to abs integer")
        
        val = 0
    except TypeError:
        if val != '':
            logger.warning("TypeError: value is not correct type")
        
        val = 0
    
    return val

def floatOrZero(val):
    try:
        val = float(val)
    except ValueError:
        if val != '':
            logger.warning("ValueError: value can't transfer to float")
        
        val = 0
    except TypeError:
        if val != '':
            logger.warning("TypeError: value is not correct type")
        
        val = 0
    
    return val