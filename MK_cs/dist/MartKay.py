# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ZLL\Desktop\test.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
import os
from PyQt4 import QtCore, QtGui
reload(sys)

sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 495)
        self.Con = QtGui.QLabel(Dialog)
        self.Con.setGeometry(QtCore.QRect(30, 30, 71, 16))
        self.Con.setObjectName(_fromUtf8("Con"))
        self.ConCount = QtGui.QLineEdit(Dialog)
        self.ConCount.setGeometry(QtCore.QRect(140, 30, 101, 20))
        self.ConCount.setObjectName(_fromUtf8("ConCount"))
        self.ConQuery = QtGui.QPushButton(Dialog)
        self.ConQuery.setGeometry(QtCore.QRect(260, 30, 75, 23))
        self.ConQuery.setObjectName(_fromUtf8("ConQuery"))
        self.NotCon = QtGui.QLabel(Dialog)
        self.NotCon.setGeometry(QtCore.QRect(30, 60, 71, 16))
        self.NotCon.setObjectName(_fromUtf8("NotCon"))
        self.NotConCount = QtGui.QLineEdit(Dialog)
        self.NotConCount.setGeometry(QtCore.QRect(140, 60, 101, 20))
        self.NotConCount.setObjectName(_fromUtf8("NotConCount"))
        self.NotConQuery = QtGui.QPushButton(Dialog)
        self.NotConQuery.setGeometry(QtCore.QRect(260, 60, 75, 23))
        self.NotConQuery.setObjectName(_fromUtf8("NotConQuery"))
        self.Order = QtGui.QLabel(Dialog)
        self.Order.setGeometry(QtCore.QRect(30, 110, 91, 16))
        self.Order.setObjectName(_fromUtf8("Order"))
        self.OrderCount = QtGui.QLineEdit(Dialog)
        self.OrderCount.setGeometry(QtCore.QRect(140, 110, 101, 20))
        self.OrderCount.setObjectName(_fromUtf8("OrderCount"))
        self.OrderQuery = QtGui.QPushButton(Dialog)
        self.OrderQuery.setGeometry(QtCore.QRect(260, 110, 75, 23))
        self.OrderQuery.setObjectName(_fromUtf8("OrderQuery"))
        self.NotOrderCount = QtGui.QLineEdit(Dialog)
        self.NotOrderCount.setGeometry(QtCore.QRect(140, 140, 101, 20))
        self.NotOrderCount.setObjectName(_fromUtf8("NotOrderCount"))
        self.NotOrderQuery = QtGui.QPushButton(Dialog)
        self.NotOrderQuery.setGeometry(QtCore.QRect(260, 140, 75, 23))
        self.NotOrderQuery.setObjectName(_fromUtf8("NotOrderQuery"))
        self.NotOrder = QtGui.QLabel(Dialog)
        self.NotOrder.setGeometry(QtCore.QRect(30, 140, 101, 20))
        self.NotOrder.setObjectName(_fromUtf8("NotOrder"))
        self.CityCount = QtGui.QLineEdit(Dialog)
        self.CityCount.setGeometry(QtCore.QRect(180, 180, 61, 20))
        self.CityCount.setObjectName(_fromUtf8("CityCount"))
        self.CityOrder = QtGui.QLabel(Dialog)
        self.CityOrder.setGeometry(QtCore.QRect(30, 180, 71, 20))
        self.CityOrder.setObjectName(_fromUtf8("CityOrder"))
        self.CityQuery1 = QtGui.QPushButton(Dialog)
        self.CityQuery1.setGeometry(QtCore.QRect(260, 180, 75, 23))
        self.CityQuery1.setObjectName(_fromUtf8("CityQuery1"))
        self.AgeDiff = QtGui.QPushButton(Dialog)
        self.AgeDiff.setGeometry(QtCore.QRect(60, 450, 75, 23))
        self.AgeDiff.setObjectName(_fromUtf8("AgeDiff"))
        self.CityDiff = QtGui.QPushButton(Dialog)
        self.CityDiff.setGeometry(QtCore.QRect(150, 450, 75, 23))
        self.CityDiff.setObjectName(_fromUtf8("CityDiff"))
        self.TimeDiff = QtGui.QPushButton(Dialog)
        self.TimeDiff.setGeometry(QtCore.QRect(240, 450, 75, 23))
        self.TimeDiff.setObjectName(_fromUtf8("TimeDiff"))
        self.CityName = QtGui.QLineEdit(Dialog)
        self.CityName.setGeometry(QtCore.QRect(70, 180, 91, 20))
        self.CityName.setObjectName(_fromUtf8("CityName"))
        self.a1 = QtGui.QLabel(Dialog)
        self.a1.setGeometry(QtCore.QRect(60, 220, 91, 20))
        self.a1.setObjectName(_fromUtf8("a1"))
        self.aText = QtGui.QLineEdit(Dialog)
        self.aText.setGeometry(QtCore.QRect(150, 220, 21, 20))
        self.aText.setObjectName(_fromUtf8("aText"))
        self.a2 = QtGui.QLabel(Dialog)
        self.a2.setGeometry(QtCore.QRect(180, 220, 91, 20))
        self.a2.setObjectName(_fromUtf8("a2"))
        self.bText = QtGui.QLineEdit(Dialog)
        self.bText.setGeometry(QtCore.QRect(150, 310, 21, 20))
        self.bText.setObjectName(_fromUtf8("bText"))
        self.b1 = QtGui.QLabel(Dialog)
        self.b1.setGeometry(QtCore.QRect(60, 310, 91, 20))
        self.b1.setObjectName(_fromUtf8("b1"))
        self.b2 = QtGui.QLabel(Dialog)
        self.b2.setGeometry(QtCore.QRect(180, 310, 91, 20))
        self.b2.setObjectName(_fromUtf8("b2"))
        self.AQuery = QtGui.QPushButton(Dialog)
        self.AQuery.setGeometry(QtCore.QRect(260, 220, 75, 23))
        self.AQuery.setObjectName(_fromUtf8("AQuery"))
        self.BQuery = QtGui.QPushButton(Dialog)
        self.BQuery.setGeometry(QtCore.QRect(260, 310, 75, 23))
        self.BQuery.setObjectName(_fromUtf8("BQuery"))
        self.cText = QtGui.QLineEdit(Dialog)
        self.cText.setGeometry(QtCore.QRect(60, 410, 161, 20))
        self.cText.setObjectName(_fromUtf8("cText"))
        self.CQuery = QtGui.QPushButton(Dialog)
        self.CQuery.setGeometry(QtCore.QRect(300, 410, 75, 23))
        self.CQuery.setObjectName(_fromUtf8("CQuery"))
        self.c2 = QtGui.QLabel(Dialog)
        self.c2.setGeometry(QtCore.QRect(230, 410, 91, 20))
        self.c2.setObjectName(_fromUtf8("c2"))
        self.c1 = QtGui.QLabel(Dialog)
        self.c1.setGeometry(QtCore.QRect(10, 410, 91, 20))
        self.c1.setObjectName(_fromUtf8("c1"))
        self.aResult = QtGui.QTextEdit(Dialog)
        self.aResult.setGeometry(QtCore.QRect(10, 250, 380, 51))
        self.aResult.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.aResult.setObjectName(_fromUtf8("aResult"))
        self.bResult = QtGui.QTextEdit(Dialog)
        self.bResult.setGeometry(QtCore.QRect(10, 340, 380, 51))
        self.bResult.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.bResult.setObjectName(_fromUtf8("bResult"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.AgeDiff.clicked.connect(self.ageDiff) 
        self.CityDiff.clicked.connect(self.cityDiff) 
        self.TimeDiff.clicked.connect(self.timeDiff) 
        
        self.CityQuery1.clicked.connect(self.cityQuery) 
        self.ConQuery.clicked.connect(self.conQuery)
        self.NotConQuery.clicked.connect(self.notConQuery)
        self.OrderQuery.clicked.connect(self.orderQuery) 
        self.NotOrderQuery.clicked.connect(self.notOrderQuery) 
		
        self.AQuery.clicked.connect(self.aQuery) 
        self.BQuery.clicked.connect(self.bQuery) 
        self.CQuery.clicked.connect(self.cQuery)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "MartKay", None))
        self.Con.setText(_translate("Dialog", "顾问转发数", None))
        self.ConQuery.setText(_translate("Dialog", "查询", None))
        self.NotCon.setText(_translate("Dialog", "非顾问转发数", None))
        self.NotConQuery.setText(_translate("Dialog", "查询", None))
        self.Order.setText(_translate("Dialog", "下单客户转发数", None))
        self.OrderQuery.setText(_translate("Dialog", "查询", None))
        self.NotOrderQuery.setText(_translate("Dialog", "查询", None))
        self.NotOrder.setText(_translate("Dialog", "未下单客户转发数", None))
        self.CityOrder.setText(_translate("Dialog", "省份", None))
        self.CityQuery1.setText(_translate("Dialog", "查询", None))
        self.AgeDiff.setText(_translate("Dialog", "年龄趋势图", None))
        self.CityDiff.setText(_translate("Dialog", "省份趋势图", None))
        self.TimeDiff.setText(_translate("Dialog", "时间趋势图", None))
        self.a1.setText(_translate("Dialog", "查询传播广度前", None))
        self.a2.setText(_translate("Dialog", "的ShareID", None))
        self.b1.setText(_translate("Dialog", "查询传播深度前", None))
        self.b2.setText(_translate("Dialog", "的ShareID", None))
        self.AQuery.setText(_translate("Dialog", "查询", None))
        self.BQuery.setText(_translate("Dialog", "查询", None))
        self.CQuery.setText(_translate("Dialog", "查询", None))
        self.c2.setText(_translate("Dialog", "的传播路径", None))
        self.c1.setText(_translate("Dialog", "ShareID", None))


    def ageDiff(self): 
        os.popen("AgeDiff.py")
    def cityDiff(self): 
        os.popen("CityDiff.py")
    def timeDiff(self): 
        QtGui.QMessageBox.critical(QtGui.QWidget(), 'Error', u'功能尚未开发，敬请期待！')
        
    def conQuery(self): 
        conCount=str(os.popen("ConQuery.py").read())
        self.ConCount.setText('%s' % conCount)

    def notConQuery(self): 
        notConCount=str(os.popen("NotConQuery.py").read())
        self.NotConCount.setText('%s' % notConCount)

    def orderQuery(self): 
        orderCount=str(os.popen("OrderQuery.py").read())
        self.OrderCount.setText('%s' % orderCount)

    def notOrderQuery(self): 
        notOrderCount=str(os.popen("NotOrderQuery.py").read())
        self.NotOrderCount.setText('%s' % notOrderCount)

    def cityQuery(self): 
        city = unicode(self.CityName.text())
        queryScript= 'CityQuery.py '+city
        cityCount=str(os.popen(queryScript).read())
        self.CityCount.setText('%s' % cityCount)
        
    def aQuery(self): 
        a = unicode(self.aText.text())
        queryScript='a.py '+a
        aCount=unicode(str(os.popen(queryScript).read()))
        #QtGui.QMessageBox.about(QtGui.QWidget(), 'PyQt', aCount)aCount
        self.aResult.setText('%s' % aCount)
        
    def bQuery(self): 
        b = unicode(self.bText.text())
        queryScript='b.py '+b
        bCount=unicode(str(os.popen(queryScript).read()))
        #QtGui.QMessageBox.about(QtGui.QWidget(), 'PyQt', aCount)aCount
        self.bResult.setText('%s' % bCount)
        
    def cQuery(self): 
        c = unicode(self.cText.text())
        queryScript='ShareId.py '+c
        os.popen(queryScript)

        
        
if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QWidget()
  ui = Ui_Dialog()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())