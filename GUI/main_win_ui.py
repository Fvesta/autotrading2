# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_win.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 90))
        self.widget.setMaximumSize(QSize(16777215, 90))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")

        self.horizontalLayout.addWidget(self.widget_4)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(80, 0, 0, 0)
        self.lcdNumber = QLCDNumber(self.widget_5)
        self.lcdNumber.setObjectName(u"lcdNumber")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.lcdNumber)


        self.horizontalLayout.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 796, 706))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(0, 200))
        self.groupBox_2.setMaximumSize(QSize(16777215, 200))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.widget_6 = QWidget(self.groupBox_2)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget_6)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)
        self.widget_2.setMinimumSize(QSize(0, 0))
        self.widget_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.pushButton_7 = QPushButton(self.widget_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.pushButton_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.comboBox = QComboBox(self.widget_2)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy4)
        self.comboBox.setMinimumSize(QSize(150, 0))
        self.comboBox.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_4.addWidget(self.comboBox)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")

        self.horizontalLayout_3.addWidget(self.widget_3)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, -1, -1, -1)
        self.pushButton_3 = QPushButton(self.widget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_2.addWidget(self.pushButton_3, 0, 2, 1, 1)

        self.pushButton_5 = QPushButton(self.widget_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_2.addWidget(self.pushButton_5, 1, 0, 1, 1)

        self.pushButton_6 = QPushButton(self.widget_2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout_2.addWidget(self.pushButton_6, 1, 1, 1, 1)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_2)


        self.horizontalLayout_6.addWidget(self.widget_2)

        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")

        self.horizontalLayout_6.addWidget(self.widget_7)

        self.horizontalLayout_6.setStretch(0, 8)
        self.horizontalLayout_6.setStretch(1, 1)

        self.horizontalLayout_4.addWidget(self.widget_6)

        self.tableWidget = QTableWidget(self.groupBox_2)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        if (self.tableWidget.rowCount() < 4):
            self.tableWidget.setRowCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setItem(1, 2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(2, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(3, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(3, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(3, 2, __qtablewidgetitem11)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setMinimumSize(QSize(0, 0))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)

        self.horizontalLayout_4.addWidget(self.tableWidget)

        self.horizontalLayout_4.setStretch(0, 5)
        self.horizontalLayout_4.setStretch(1, 6)

        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uad8c\ub3d9\ubbfc", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\uacc4\uc88c\ubc88\ud638", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4 \uc124\uc815", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4\uc124\uc815", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\uac70\ub798\ub0b4\uc5ed", None))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem = self.tableWidget.item(0, 0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\uc608\ud0c1\uc790\uc0b0", None));
        ___qtablewidgetitem1 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\ub2f9\uc6d4\uc2e4\ud604\uc190\uc775", None));
        ___qtablewidgetitem2 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\ub2f9\uc77c\uc2e4\ud604\uc190\uc775", None));
        ___qtablewidgetitem3 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"10000", None));
        ___qtablewidgetitem4 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"401", None));
        ___qtablewidgetitem5 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"021021", None));
        ___qtablewidgetitem6 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\ucd1d\ub9e4\uc785\uac00", None));
        ___qtablewidgetitem7 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\ucd1d\ud3c9\uac00\uae08", None));
        ___qtablewidgetitem8 = self.tableWidget.item(2, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\uc218\uc775\ub960", None));
        ___qtablewidgetitem9 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"044011", None));
        ___qtablewidgetitem10 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"47470", None));
        ___qtablewidgetitem11 = self.tableWidget.item(3, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"11", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

