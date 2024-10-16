from core.errors import ErrorCode
from .stock_util import *
from .type_util import *

def getAccnoFromObj(obj_name):
    name_arr = obj_name.split("_")
    try:
        if len(name_arr[0]) == 0:
            accno = name_arr[1]
        else:
            raise ValueError
        
        return accno
    except ValueError as e:
        logger.error("Not correct obj_name")
        return ErrorCode.OP_ERROR
