# General constants
TRADING_TAX = 0

# TR constants
TRCODE_DICT = {
    "계좌평가현황요청": "opw00004",
    "주식기본정보요청": "opt10001",
    "관심종목정보요청": "optkwfid"
}

TR_RETURN_MAP = {
    "계좌평가현황요청": {
        "single": [
            "계좌명",
            "지점명",
            "예수금",
            "D+2추정예수금",
            "유가잔고평가액",
            "예탁자산평가액",
            "총매입금액",
            "추정예탁자산",
            "매도담보대출금",
            "당일투자원금",
            "당월투자원금",
            "누적투자원금",
            "당일투자손익",
            "당월투자손익",
            "누적투자손익",
            "당일손익율",
            "당월손익율",
            "누적손익율",
            "출력건수"
        ],
        "multi": [
            "종목코드",
            "종목명",
            "보유수량",
            "평균단가",
            "현재가",
            "평가금액",
            "손익금액",
            "손익율",
            "대출일",
            "매입금액",
            "결제잔고",
            "전일매수수량",
            "전일매도수량",
            "금일매수수량",
            "금일매도수량"
        ],
    },
    "주식기본정보요청": {
        "single": [
            "종목코드",
            "종목명",
            "결산월",
            "액면가",
            "자본금",
            "상장주식",
            "신용비율",
            "연중최고",
            "연중최저",
            "시가총액",
            "시가총액비중",
            "외인소진률",
            "대용가",
            "PER",
            "EPS",
            "ROE",
            "PBR",
            "EV",
            "BPS",
            "매출액",
            "영업이익",
            "당기순이익",
            "250최고",
            "250최저",
            "시가",
            "고가",
            "저가",
            "상한가",
            "하한가",
            "기준가",
            "예상체결가",
            "예상체결수량",
            "250최고가일",
            "250최고가대비율",
            "250최저가일",
            "250최저가대비율",
            "현재가",
            "대비기호",
            "전일대비",
            "등락율",
            "거래량",
            "거래대비",
            "액면가단위",
            "유통주식",
            "유통비율"
        ]
    },
    "관심종목정보요청": {
        "multi": [
            "종목코드",
            "종목명",
            "현재가",
            "기준가",
            "전일대비",
            "전일대비기호",
            "등락율",
            "거래량",
            "거래대금",
            "체결량",
            "체결강도",
            "전일거래량대비",
            "매도호가",
            "매수호가",
            "매도1차호가",
            "매도2차호가",
            "매도3차호가",
            "매도4차호가",
            "매도5차호가",
            "매수1차호가",
            "매수2차호가",
            "매수3차호가",
            "매수4차호가",
            "매수5차호가",
            "상한가",
            "하한가",
            "시가",
            "고가",
            "저가",
            "종가",
            "체결시간",
            "예상체결가",
            "예상체결량",
            "자본금",
            "액면가",
            "시가총액",
            "주식수",
            "호가시간",
            "일자",
            "우선매도잔량",
            "우선매수잔량",
            "우선매도건수",
            "우선매수건수",
            "총매도잔량",
            "총매수잔량",
            "총매도건수",
            "총매수건수",
            "패리티",
            "기어링",
            "손익분기",
            "자본지지",
            "ELW행사가",
            "전환비율",
            "ELW만기일",
            "미결제약정",
            "미결제전일대비",
            "이론가",
            "내재변동성",
            "델타",
            "감마",
            "쎄타",
            "베가",
            "로"
        ]
    },
    "주문요청": {
        "single": ["주문번호"]
    }
}

# Real constants
REAL_NO_MAP = {
    "현재가": 10,
    "전일대비": 11,
    "등락율": 12,
    "거래량": 15,
    "누적거래량": 13,
    "누적거래대금": 14,
    "시가": 16,
    "고가": 17,
    "저가": 18,
    "체결시간": 20,
    "전일대비기호": 25,
    "전일거래량대비(계약, 주)": 26,
    "(최우선)매도호가": 27,
    "(최우선)매수호가": 28,
    "거래대금증감": 29,
    "전일거래량대비(비율)": 30,
    "거래회전율": 31,
    "거래비용": 32,
    "매도호가1": 41,
    "매도호가2": 42,
    "매도호가3": 43,
    "매도호가4": 44,
    "매도호가5": 45,
    "매도호가6": 46,
    "매도호가7": 47,
    "매도호가8": 48,
    "매도호가9": 49,
    "매도호가10": 50,
    "매도호가수량1": 61,
    "매도호가수량2": 62,
    "매도호가수량3": 63,
    "매도호가수량4": 64,
    "매도호가수량5": 65,
    "매도호가수량6": 66,
    "매도호가수량7": 67,
    "매도호가수량8": 68,
    "매도호가수량9": 69,
    "매도호가수량10": 70,
    "매수호가1": 51,
    "매수호가2": 52,
    "매수호가3": 53,
    "매수호가4": 54,
    "매수호가5": 55,
    "매수호가6": 56,
    "매수호가7": 57,
    "매수호가8": 58,
    "매수호가9": 59,
    "매수호가10": 60,
    "매수비율": 129,
    "체결강도": 228,
    "장구분": 290,
    "종목명": 302,
    "상한가가격": 305,
    "하한가가격": 306,
    "기준가": 307,
    "시가총액(억)": 311,
    "상한가발생시간": 567,
    "하한가발생시간": 568,
    "KO접근도": 691,
    "전일 동시간 거래량 비율": 851,
    "주문수량": 900,
    "주문가격": 901,
    "미체결수량": 902,
    "체결누계금액": 903,
    "원주문번호": 904,
    "주문구분": 905,
    "매매구분": 906,
    "매도수구분": 907,
    "주문/체결시간": 908,
    "체결번호": 909,
    "체결가": 910,
    "체결량": 911,
    "주문업무분류": 912,
    "주문상태": 913,
    "단위체결가": 914,
    "단위체결량": 915,
    "대출일": 916,
    "신용구분": 917,
    "만기일": 918,
    "거부사유": 919,
    "화면번호": 920,
    "터미널번호": 921,
    "신용구분(실시간 체결용)": 922,
    "대출일(실시간 체결용)": 923,
    "보유수량": 930,
    "매입단가": 931,
    "총매입가(당일누적)": 932,
    "주문가능수량": 933,
    "당일매매수수료": 938,
    "당일매매세금": 939,
    "당일순매수량": 945,
    "매도/매수구분": 946,
    "당일총매도손익": 950,
    "신용금액": 957,
    "신용이자": 958,
    "담보대출수량": 959,
    "당일실현손익(유가)": 990,
    "당일실현손익률(유가)": 991,
    "당일실현손익(신용)": 992,
    "당일실현손익률(신용)": 993,
    "손익율(실현손익)": 8019,
    "종목코드,업종코드": 9001,
    "계좌번호": 9201,
    "주문번호": 9203,
    "관리자사번": 9205,
}

REAL_RET_MAP = {
    "주식체결": [
      "체결시간",
      "현재가",
      "전일대비",
      "등락율",
      "(최우선)매도호가",
      "(최우선)매수호가",
      "거래량",
      "누적거래량",
      "누적거래대금",
      "시가",
      "고가",
      "저가",
      "전일대비기호",
      "전일거래량대비(계약, 주)",
      "거래대금증감",
      "전일거래량대비(비율)",
      "거래회전율",
      "거래비용",
      "체결강도",
      "시가총액(억)",
      "장구분",
      "KO접근도",
      "상한가발생시간",
      "하한가발생시간",
      "전일 동시간 거래량 비율"  
    ],
    "주문체결": [
        "계좌번호",
        "주문번호",
        "관리자사번",
        "종목코드,업종코드",
        "주문업무분류",
        "주문상태",
        "종목명",
        "주문수량",
        "주문가격",
        "미체결수량",
        "체결누계금액",
        "원주문번호",
        "주문구분",
        "매매구분",
        "매도수구분",
        "주문/체결시간",
        "체결번호",
        "체결가",
        "체결량",
        "현재가",
        "(최우선)매도호가",
        "(최우선)매수호가",
        "단위체결가",
        "단위체결량",
        "당일매매수수료",
        "당일매매세금",
        "거부사유",
        "화면번호",
        "터미널번호",
        "신용구분(실시간 체결용)",
        "대출일(실시간 체결용)"
    ],
    "잔고": [
        "계좌번호",
        "종목코드,업종코드",
        "신용구분",
        "대출일",
        "종목명",
        "현재가",
        "보유수량",
        "매입단가",
        "총매입가(당일누적)",
        "주문가능수량",
        "당일순매수량",
        "매도/매수구분",
        "당일총매도손익",
        "(최우선)매도호가",
        "(최우선)매수호가",
        "기준가",
        "손익율(실현손익)",
        "신용금액",
        "신용이자",
        "만기일",
        "당일실현손익(유가)",
        "당일실현손익률(유가)",
        "당일실현손익(신용)",
        "당일실현손익률(신용)",
        "담보대출수량"
    ]
}

ORDER_TYPE = {
    "신규매수": 1,
    "신규매도": 2,
    "매수취소": 3,
    "매도취소": 4,
    "매수정정": 5,
    "매도정정": 6
}

ORDER_TAG = {
    "지정가": "00",
    "시장가": "03",
    "조건부지정가": "05",
    "최유리지정가": "06",
    "최우선지정가": "07",
    "지정가IOC": "10",
    "시장가IOC": "13",
    "최유리IOC": "16",
    "지정가FOK": "20",
    "시장가FOK": "23",
    "최유리FOK": "26",
    "장전시간외종가": "61",
    "시간외단일가": "62",
    "장후시간외종가": "81"
}