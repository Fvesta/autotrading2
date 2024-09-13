TRAILING_STOP_BASIC_OPTION = {
        "standard": "each",             # each or total
        "tick": {
            "type": "seconds",
            "val": 30
        },                   
        "lines": {
            "type": "manual",           # manual or auto           
            "line_1": 1, 
            "line_2": 3,
            "line_3": 5,
            "line_4": 8, 
            "line_5": 12,
            "line_6": 16,
            "line_7": 20,
            "line_8": 25,
        },
        "division": {
            "div_1": 50,              # percent
            "div_2": 100,
        }
    }

TRADING_BASIC_OPTION = {
    "trailing_stop": {
        "used": True,
        "option": TRAILING_STOP_BASIC_OPTION 
    }
}

