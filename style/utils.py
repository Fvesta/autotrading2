from PySide2.QtWidgets import *

def setTableSizeContent(table):
    header = table.horizontalHeader()
    twidth = header.width()
    
    width = []
    for column in range(header.count()):
        header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
        width.append(header.sectionSize(column))

    wfactor = twidth / sum(width)
    for column in range(header.count()):
        header.setSectionResizeMode(column, QHeaderView.Interactive)
        header.resizeSection(column, int(width[column]*wfactor))
        
def setTableSizeSameHor(table):
    header = table.horizontalHeader()
    twidth = header.width()
    
    count = header.count()
    
    for column in range(count):
        table.setColumnWidth(column, twidth*1/count)

def setTableSizeSameVer(table):
    header = table.verticalHeader()
    theight = header.height()
    
    count = header.count()
    
    for row in range(count):
        table.setRowHeight(row, theight*1/count)
