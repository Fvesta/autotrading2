# Trailing Stop option
TRAILING_STOP_BASIC_OPTION = {
        "standard": "each",             # each or total
        "tick": {
            "type": "seconds",
            "val": 30
        },                   
        "line_opt": {
            "type": "manual",           # manual or auto
            "lines": [1, 3, 5, 8, 12, 16, 20, 25]
        },
        "division": [
            {
                "sell_percent": 50
            },
            {
                "sell_percent": 100
            }
        ]
    }

STOP_LOSS_BASIC_OPTION = {
    "division": [
        {
            "income_rate": -1,
            "sell_percent": 50
        },
        {
            "income_rate": -2,
            "sell_percent": 100
        }
    ]
}

# Base Algorithm options
ALGO_SHORT_HIT_BASIC_OPTION = {
    "condition": None,                  # Essential, has to fix
    "max_stock_cnt": 10,
    "just_today": True,
    "order": {
        "one_time_amount": 100000,
        "buy_same_stock": False,
        "order_type": "market_price"
    }
    
}

TRADING_BASIC_OPTION = {
    "trailing_stop": {
        "used": True,
        "option": TRAILING_STOP_BASIC_OPTION 
    },
    "stop_loss": {
        "used": True,
        "option": STOP_LOSS_BASIC_OPTION
    },
    "base_algorithm": {
        "algo": "short_hit",
        "option": ALGO_SHORT_HIT_BASIC_OPTION
    }
}

