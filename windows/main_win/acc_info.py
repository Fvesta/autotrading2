from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

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
    verticalLayout_4 = QVBoxLayout()
    verticalLayout_4.setObjectName(u"verticalLayout_4")
    horizontalLayout_2 = QHBoxLayout()
    horizontalLayout_2.setSpacing(15)
    horizontalLayout_2.setObjectName(u"horizontalLayout_2")
    label_2 = QLabel(widget_2)
    label_2.setObjectName(u"label_2")

    horizontalLayout_2.addWidget(label_2)

    pushButton_7 = QPushButton(widget_2)
    pushButton_7.setObjectName(u"pushButton_7")
    sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    sizePolicy3.setHorizontalStretch(0)
    sizePolicy3.setVerticalStretch(0)
    sizePolicy3.setHeightForWidth(pushButton_7.sizePolicy().hasHeightForWidth())
    pushButton_7.setSizePolicy(sizePolicy3)

    horizontalLayout_2.addWidget(pushButton_7)


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

    widget_3 = QWidget(widget_2)
    widget_3.setObjectName(u"widget_3")

    horizontalLayout_3.addWidget(widget_3)

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

    pushButton = QPushButton(widget_2)
    pushButton.setObjectName(u"pushButton")

    gridLayout_2.addWidget(pushButton, 0, 0, 1, 1)

    pushButton_2 = QPushButton(widget_2)
    pushButton_2.setObjectName(u"pushButton_2")

    gridLayout_2.addWidget(pushButton_2, 0, 1, 1, 1)


    verticalLayout_5.addLayout(gridLayout_2)


    horizontalLayout_6.addWidget(widget_2)

    widget_7 = QWidget(widget_6)
    widget_7.setObjectName(u"widget_7")

    horizontalLayout_6.addWidget(widget_7)

    horizontalLayout_6.setStretch(0, 8)
    horizontalLayout_6.setStretch(1, 1)

    horizontalLayout_4.addWidget(widget_6)

    balanceTable = QTableWidget(accGroup)
    if (balanceTable.columnCount() < 3):
        balanceTable.setColumnCount(3)
    if (balanceTable.rowCount() < 4):
        balanceTable.setRowCount(4)
    __qtablewidgetitem = QTableWidgetItem()
    balanceTable.setItem(0, 0, __qtablewidgetitem)
    __qtablewidgetitem1 = QTableWidgetItem()
    balanceTable.setItem(0, 1, __qtablewidgetitem1)
    __qtablewidgetitem2 = QTableWidgetItem()
    balanceTable.setItem(0, 2, __qtablewidgetitem2)
    __qtablewidgetitem3 = QTableWidgetItem()
    balanceTable.setItem(1, 0, __qtablewidgetitem3)
    __qtablewidgetitem4 = QTableWidgetItem()
    balanceTable.setItem(1, 1, __qtablewidgetitem4)
    __qtablewidgetitem5 = QTableWidgetItem()
    balanceTable.setItem(1, 2, __qtablewidgetitem5)
    __qtablewidgetitem6 = QTableWidgetItem()
    balanceTable.setItem(2, 0, __qtablewidgetitem6)
    __qtablewidgetitem7 = QTableWidgetItem()
    balanceTable.setItem(2, 1, __qtablewidgetitem7)
    __qtablewidgetitem8 = QTableWidgetItem()
    balanceTable.setItem(2, 2, __qtablewidgetitem8)
    __qtablewidgetitem9 = QTableWidgetItem()
    balanceTable.setItem(3, 0, __qtablewidgetitem9)
    __qtablewidgetitem10 = QTableWidgetItem()
    balanceTable.setItem(3, 1, __qtablewidgetitem10)
    __qtablewidgetitem11 = QTableWidgetItem()
    balanceTable.setItem(3, 2, __qtablewidgetitem11)
    balanceTable.setObjectName(u"balanceTable")
    sizePolicy2.setHeightForWidth(balanceTable.sizePolicy().hasHeightForWidth())
    balanceTable.setSizePolicy(sizePolicy2)
    balanceTable.setMinimumSize(QSize(0, 0))
    balanceTable.setAlternatingRowColors(True)
    balanceTable.setRowCount(4)
    balanceTable.setColumnCount(3)
    balanceTable.horizontalHeader().setVisible(False)
    balanceTable.horizontalHeader().setCascadingSectionResizes(False)
    balanceTable.horizontalHeader().setDefaultSectionSize(100)
    balanceTable.horizontalHeader().setProperty("showSortIndicator", False)
    balanceTable.verticalHeader().setVisible(False)
    balanceTable.verticalHeader().setMinimumSectionSize(30)
    balanceTable.verticalHeader().setDefaultSectionSize(30)

    horizontalLayout_4.addWidget(balanceTable)

    horizontalLayout_4.setStretch(0, 5)
    horizontalLayout_4.setStretch(1, 6)
    
    
    ui.verticalLayout_3.addWidget(accGroup)
    
    ################# retranslateUI ####################
    ui.label.setText(QCoreApplication.translate("MainWindow", u"\uad8c\ub3d9\ubbfc", None))
    accGroup.setTitle(QCoreApplication.translate("MainWindow", u"\uacc4\uc88c\ubc88\ud638", None))
    label_2.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4 \uc124\uc815", None))
    pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791", None))
    pushButton_3.setText(QCoreApplication.translate("MainWindow", u"test", None))
    pushButton_5.setText(QCoreApplication.translate("MainWindow", u"test", None))
    pushButton_6.setText(QCoreApplication.translate("MainWindow", u"test", None))
    pushButton.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4\uc124\uc815", None))
    pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\uac70\ub798\ub0b4\uc5ed", None))

    __sortingEnabled = balanceTable.isSortingEnabled()
    balanceTable.setSortingEnabled(False)
    ___qtablewidgetitem = balanceTable.item(0, 0)
    ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", "예탁자산", None))
    ___qtablewidgetitem1 = balanceTable.item(0, 1)
    ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"당월실현손익", None))
    ___qtablewidgetitem2 = balanceTable.item(0, 2)
    ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"당일실현손익", None))
    ___qtablewidgetitem6 = balanceTable.item(2, 0)
    ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"총매입가", None))
    ___qtablewidgetitem7 = balanceTable.item(2, 1)
    ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"총평가금", None))
    ___qtablewidgetitem8 = balanceTable.item(2, 2)
    ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"수익률", None))
    balanceTable.setSortingEnabled(__sortingEnabled)
    
    ####################################################
    
    
    # Tracing maked local variables
    endLocals = set(locals().keys())
    
    makedVars = endLocals - startLocals
    for var in makedVars:
        setattr(ui, f"_{accno}_{var}", locals()[var])