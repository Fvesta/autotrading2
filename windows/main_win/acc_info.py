from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import QSvgWidget

def newAccInfo(ui, accno):    
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    
    # Load all local variables
    startLocals = set(locals().keys())
    
    accGroup = QGroupBox(ui.scrollAreaWidgetContents)
    accGroup.setObjectName(u"accGroup")
    sizePolicy.setHeightForWidth(accGroup.sizePolicy().hasHeightForWidth())
    accGroup.setSizePolicy(sizePolicy)
    accGroup.setMinimumSize(QSize(0, 200))
    accGroup.setMaximumSize(QSize(16777215, 200))
    horizontalLayout_4 = QHBoxLayout(accGroup)
    horizontalLayout_4.setSpacing(0)
    horizontalLayout_4.setObjectName(u"horizontalLayout_4")
    horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
    widget_6 = QWidget(accGroup)
    widget_6.setObjectName(u"widget_6")
    horizontalLayout_6 = QHBoxLayout(widget_6)
    horizontalLayout_6.setSpacing(0)
    horizontalLayout_6.setObjectName(u"horizontalLayout_6")
    horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
    widget_2 = QWidget(widget_6)
    widget_2.setObjectName(u"widget_2")
    sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy2.setHorizontalStretch(0)
    sizePolicy2.setVerticalStretch(0)
    sizePolicy2.setHeightForWidth(widget_2.sizePolicy().hasHeightForWidth())
    widget_2.setSizePolicy(sizePolicy2)
    widget_2.setMinimumSize(QSize(0, 0))
    widget_2.setMaximumSize(QSize(16777215, 16777215))
    verticalLayout_5 = QVBoxLayout(widget_2)
    verticalLayout_5.setSpacing(15)
    verticalLayout_5.setObjectName(u"verticalLayout_5")
    verticalLayout_5.setContentsMargins(0, 0, 0, 0)
    horizontalLayout_3 = QHBoxLayout()
    horizontalLayout_3.setSpacing(0)
    horizontalLayout_3.setObjectName(u"horizontalLayout_3")
    horizontalLayout_3.setContentsMargins(0, 8, 0, 0)
    verticalLayout_4 = QVBoxLayout()
    verticalLayout_4.setObjectName(u"verticalLayout_4")
    horizontalLayout_2 = QHBoxLayout()
    horizontalLayout_2.setSpacing(15)
    horizontalLayout_2.setObjectName(u"horizontalLayout_2")
    horizontalLayout_2.setContentsMargins(6, 0, 10, 3)
    tradeset_label = QLabel(widget_2)
    tradeset_label.setObjectName(u"tradeset_label")

    horizontalLayout_2.addWidget(tradeset_label)
    
    setting_btn = QSvgWidget()
    setting_btn.setObjectName(u"setting_btn")
    sizePolicy_custom_1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy_custom_1.setHorizontalStretch(0)
    sizePolicy_custom_1.setVerticalStretch(0)
    sizePolicy_custom_1.setHeightForWidth(setting_btn.sizePolicy().hasHeightForWidth())
    setting_btn.setSizePolicy(sizePolicy_custom_1)
    setting_btn.setMinimumSize(QSize(18, 18))
    setting_btn.setMaximumSize(QSize(18, 18))
    setting_btn.load("style/assets/setting_icon.svg")
    
    horizontalLayout_2.addWidget(setting_btn)

    verticalLayout_4.addLayout(horizontalLayout_2)

    comboBox = QComboBox(widget_2)
    comboBox.setObjectName(u"comboBox")
    sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy4.setHorizontalStretch(0)
    sizePolicy4.setVerticalStretch(0)
    sizePolicy4.setHeightForWidth(comboBox.sizePolicy().hasHeightForWidth())
    comboBox.setSizePolicy(sizePolicy4)
    comboBox.setMinimumSize(QSize(150, 0))
    comboBox.setMaximumSize(QSize(150, 16777215))

    verticalLayout_4.addWidget(comboBox)

    horizontalLayout_3.addLayout(verticalLayout_4)

    horizontal_custom_layout_1 = QHBoxLayout()
    horizontal_custom_layout_1.setObjectName(u"horizontal_custom_layout_1")
    horizontal_custom_layout_1.setContentsMargins(60, 0, 0, 0)
    
    horizontal_custom_layout_2 = QHBoxLayout()
    horizontal_custom_layout_2.setObjectName(u"horizontal_custom_layout_2")
    
    play_btn = QSvgWidget()
    play_btn.setObjectName(u"play_btn")
    sizePolicy_custom_2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy_custom_2.setHeightForWidth(setting_btn.sizePolicy().hasHeightForWidth())
    play_btn.setSizePolicy(sizePolicy_custom_2)
    play_btn.setFixedSize(40, 40)
    play_btn.load("style/assets/play_icon.svg")
    
    horizontal_custom_layout_2.addWidget(play_btn, 0, Qt.AlignCenter)
    
    horizontal_custom_layout_1.addLayout(horizontal_custom_layout_2)
    
    widget_3 = QWidget(widget_2)
    widget_3.setObjectName(u"widget_3")

    horizontal_custom_layout_1.addWidget(widget_3)
    horizontal_custom_layout_1.setStretch(10, 1)

    horizontalLayout_3.addLayout(horizontal_custom_layout_1)

    horizontalLayout_3.setStretch(1, 1)

    verticalLayout_5.addLayout(horizontalLayout_3)

    gridLayout_2 = QGridLayout()
    gridLayout_2.setSpacing(7)
    gridLayout_2.setObjectName(u"gridLayout_2")
    gridLayout_2.setContentsMargins(0, -1, -1, -1)
    pushButton_3 = QPushButton(widget_2)
    pushButton_3.setObjectName(u"pushButton_3")

    gridLayout_2.addWidget(pushButton_3, 0, 2, 1, 1)

    pushButton_5 = QPushButton(widget_2)
    pushButton_5.setObjectName(u"pushButton_5")

    gridLayout_2.addWidget(pushButton_5, 1, 0, 1, 1)

    pushButton_6 = QPushButton(widget_2)
    pushButton_6.setObjectName(u"pushButton_6")

    gridLayout_2.addWidget(pushButton_6, 1, 1, 1, 1)

    balance_btn = QPushButton(widget_2)
    balance_btn.setObjectName(u"balance_btn")

    gridLayout_2.addWidget(balance_btn, 0, 0, 1, 1)

    trade_log_btn = QPushButton(widget_2)
    trade_log_btn.setObjectName(u"trade_log_btn")

    gridLayout_2.addWidget(trade_log_btn, 0, 1, 1, 1)


    verticalLayout_5.addLayout(gridLayout_2)


    horizontalLayout_6.addWidget(widget_2)

    widget_7 = QWidget(widget_6)
    widget_7.setObjectName(u"widget_7")

    horizontalLayout_6.addWidget(widget_7)

    horizontalLayout_6.setStretch(0, 8)
    horizontalLayout_6.setStretch(1, 1)

    horizontalLayout_4.addWidget(widget_6)

    balance_table = QTableWidget(accGroup)
    if (balance_table.columnCount() < 3):
        balance_table.setColumnCount(3)
    if (balance_table.rowCount() < 4):
        balance_table.setRowCount(4)
    __qtablewidgetitem = QTableWidgetItem()
    balance_table.setItem(0, 0, __qtablewidgetitem)
    __qtablewidgetitem1 = QTableWidgetItem()
    balance_table.setItem(0, 1, __qtablewidgetitem1)
    __qtablewidgetitem2 = QTableWidgetItem()
    balance_table.setItem(0, 2, __qtablewidgetitem2)
    __qtablewidgetitem3 = QTableWidgetItem()
    balance_table.setItem(1, 0, __qtablewidgetitem3)
    __qtablewidgetitem4 = QTableWidgetItem()
    balance_table.setItem(1, 1, __qtablewidgetitem4)
    __qtablewidgetitem5 = QTableWidgetItem()
    balance_table.setItem(1, 2, __qtablewidgetitem5)
    __qtablewidgetitem6 = QTableWidgetItem()
    balance_table.setItem(2, 0, __qtablewidgetitem6)
    __qtablewidgetitem7 = QTableWidgetItem()
    balance_table.setItem(2, 1, __qtablewidgetitem7)
    __qtablewidgetitem8 = QTableWidgetItem()
    balance_table.setItem(2, 2, __qtablewidgetitem8)
    __qtablewidgetitem9 = QTableWidgetItem()
    balance_table.setItem(3, 0, __qtablewidgetitem9)
    __qtablewidgetitem10 = QTableWidgetItem()
    balance_table.setItem(3, 1, __qtablewidgetitem10)
    __qtablewidgetitem11 = QTableWidgetItem()
    balance_table.setItem(3, 2, __qtablewidgetitem11)
    balance_table.setObjectName(u"balance_table")
    sizePolicy2.setHeightForWidth(balance_table.sizePolicy().hasHeightForWidth())
    balance_table.setSizePolicy(sizePolicy2)
    balance_table.setMinimumSize(QSize(0, 0))
    balance_table.setAlternatingRowColors(True)
    balance_table.setRowCount(4)
    balance_table.setColumnCount(3)
    balance_table.horizontalHeader().setVisible(False)
    balance_table.horizontalHeader().setCascadingSectionResizes(False)
    balance_table.horizontalHeader().setDefaultSectionSize(100)
    balance_table.horizontalHeader().setProperty("showSortIndicator", False)
    balance_table.verticalHeader().setVisible(False)
    balance_table.verticalHeader().setMinimumSectionSize(30)
    balance_table.verticalHeader().setDefaultSectionSize(30)

    horizontalLayout_4.addWidget(balance_table)

    horizontalLayout_4.setStretch(0, 5)
    horizontalLayout_4.setStretch(1, 6)
    
    ui.verticalLayout_3.addWidget(accGroup)
    
    ################# retranslateUI ####################
    accGroup.setTitle(QCoreApplication.translate("MainWindow", f"계좌번호: {str(accno)}", None))
    tradeset_label.setText(QCoreApplication.translate("MainWindow", u"매매 설정", None))
    balance_btn.setText(QCoreApplication.translate("MainWindow", u"잔고", None))
    trade_log_btn.setText(QCoreApplication.translate("MainWindow", u"거래내역", None))
    pushButton_3.setText(QCoreApplication.translate("MainWindow", u"test", None))
    pushButton_5.setText(QCoreApplication.translate("MainWindow", u"test", None))
    pushButton_6.setText(QCoreApplication.translate("MainWindow", u"test", None))

    __sortingEnabled = balance_table.isSortingEnabled()
    balance_table.setSortingEnabled(False)
    ___qtablewidgetitem = balance_table.item(0, 0)
    ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", "예탁자산", None))
    ___qtablewidgetitem1 = balance_table.item(0, 1)
    ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", "매수가능금액", None))
    ___qtablewidgetitem2 = balance_table.item(0, 2)
    ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", "당일실현손익", None))
    ___qtablewidgetitem6 = balance_table.item(2, 0)
    ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", "잔고평가금", None))
    ___qtablewidgetitem7 = balance_table.item(2, 1)
    ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", "잔고평가손익", None))
    ___qtablewidgetitem8 = balance_table.item(2, 2)
    ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", "잔고수익률", None))
    balance_table.setSortingEnabled(__sortingEnabled)
    
    ####################################################
    
    
    # Tracing maked local variables
    endLocals = set(locals().keys())
    
    makedVars = endLocals - startLocals
    for var in makedVars:
        varobj = locals()[var]
        if hasattr(varobj, "setObjectName"):
            varobj.setObjectName(f"_{accno}_{var}")
        setattr(ui, f"_{accno}_{var}", locals()[var])
        