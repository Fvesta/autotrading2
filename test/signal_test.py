import os

import PySide2

QT_QPA_PLATFORM_PLUGIN_PATH = os.path.join(
    os.path.dirname(PySide2.__file__), "plugins", "platforms"
)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QT_QPA_PLATFORM_PLUGIN_PATH

import sys

from PySide2.QtAxContainer import QAxWidget
from PySide2.QtCore import SIGNAL, QEventLoop
from PySide2.QtWidgets import QApplication

app = QApplication(sys.argv)
ocx = QAxWidget("{A1574A0D-6BFA-4BD7-9020-DED88711818D}")

loop = QEventLoop()


def comm_connect():
    err = ocx.dynamicCall("CommConnect()")
    if err < 0:
        raise ValueError(err)
    loop.exec_()

signal_map = {
    "onEventConnect": SIGNAL("OnEventConnect(int)")     
}


def on_event_connect(errcode):
    if errcode < 0:
        raise ValueError(errcode)
    if errcode == 0:
        print("Connected!")
    
    loop.exit()
    ocx.disconnect(signal_map["onEventConnect"], on_event_connect)

ocx.connect(signal_map["onEventConnect"], on_event_connect)

comm_connect()

acc = ocx.dynamicCall("GetLoginInfo(const QString&)", "ACCNO")
print(acc)

def get_stock_info(code):
    rqname = "get_stock_info"
    trcode = "opt10001"
    prevnext = 0
    screenno = "0001"
    ocx.dynamicCall("SetInputValue(const QString&, const QString&)", "종목코드", code)
    err = ocx.dynamicCall(
        "CommRqData(const QString&, const QString&, int, const QString&)",
        rqname,
        trcode,
        prevnext,
        screenno,
    )
    if err < 0:
        raise ValueError(err)
    loop.exec_()


code = "005930"
price = 0

on_receive_tr_data_signal = SIGNAL(
    "OnReceiveTrData(const QString&, const QString&, const QString&, const QString&, const QString&, int, const QString&, const QString&, const QString&)"
)


def on_receive_tr_data(
    scrno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg
):
    global price

    # single data
    index = 0
    itemname = "현재가"
    price = ocx.dynamicCall(
        "GetCommData(const QString&, const QString&, int, const QString&)",
        trcode,
        recordname,
        index,
        itemname,
    ).strip()

    # multi data
    repeat_cnt = ocx.dynamicCall(
        "GetRepeatCnt(const QString&, const QString&)", trcode, recordname
    )
    if repeat_cnt > 0:
        prices = []
        for index in range(repeat_cnt):
            price_index = ocx.dynamicCall(
                "GetCommData(const QString&, const QString&, int, const QString&)",
                trcode,
                recordname,
                index,
                itemname,
            ).strip()
            prices.append(price_index)

    if prevnext not in ["", "0"]:
        ocx.dynamicCall(
            "SetInputValue(const QString&, const QString&)", "종목코드", code
        )
        err = ocx.dynamicCall(
            "CommRqData(const QString&, const QString&, int, const QString&)",
            rqname,
            trcode,
            int(prevnext),
            scrno,
        )
        if err < 0:
            raise ValueError(err)
    else:
        ocx.disconnect(on_receive_tr_data_signal, on_receive_tr_data)
        loop.exit()


ocx.connect(on_receive_tr_data_signal, on_receive_tr_data)
get_stock_info(code)

print(price)