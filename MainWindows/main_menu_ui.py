import sys
from pyface.qt import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
#import visvis as vv
from MainWindows.GeoPotential_ui import GeoPotential_MainWindow
from MainWindows.Represent_SH_ui import Repres_SH_MainWindow
from MainWindows.Represent_Body_ui import Repres_BS_MainWindow


class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setFixedSize(500, 490)
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        #Central Widget
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #Title
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(40)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        
        #Spacers
        spacerItem = QtWidgets.QSpacerItem(1, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)

        #Vertical Layout
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")

        #Button Repres_SH
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        # When clicked call function repres_SH()
        self.pushButton.clicked.connect(self.repres_SH)

        #Button Repres_BS
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        # When clicked call function repres_BS()
        self.pushButton_2.clicked.connect(self.repres_BS)

        #Button GeoPot
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)
        # When clicked call function geopot()
        self.pushButton_3.clicked.connect(self.geopot)

        self.retranslateUi()
        layout = QHBoxLayout()
        layout.addWidget(self.centralwidget)
        self.setLayout(layout)

        # Init other windows
        self.GeoPotential_w = GeoPotential_MainWindow()
        self.Repres_SH_w = Repres_SH_MainWindow()
        self.Repres_BS_w = Repres_BS_MainWindow()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Multipole Menu"))
        self.label.setText(_translate("MainWindow", "MULTIPOLE"))
        self.pushButton.setText(_translate("MainWindow", "Represent Spherical Harmonics"))
        self.pushButton_2.setText(_translate("MainWindow", "Represent Body Surface"))
        self.pushButton_3.setText(_translate("MainWindow", "GeoPotential"))
    
    # Open Represent Spherical Harmonics Window
    def repres_SH(self):
        if not self.Repres_SH_w.open:
            self.Repres_SH_w.open = True
            self.Repres_SH_w.show()

    # Open Represent Body Surface Window
    def repres_BS(self):
        if not self.Repres_BS_w.open:
            self.Repres_BS_w.open = True
            self.Repres_BS_w.show()

    # Open GeoPotential Window
    def geopot(self):
        if not self.GeoPotential_w.open:
            self.GeoPotential_w.open = True
            self.GeoPotential_w.show()
    
    def closeEvent(self, event):
        self.Repres_SH_w.exit = True
        self.Repres_BS_w.exit = True
        self.GeoPotential_w.exit = True
        self.Repres_SH_w.close()
        self.Repres_BS_w.close()
        self.GeoPotential_w.close()
        self.hide()
        event.accept()
        # Crash program on purpose to avoid wglMakeCurrent failed in MakeCurrent() that idk how to fix
        int(a)

if __name__ == "__main__":
    app = vv.use()
    #app.Create()
    main_w = MainWindow()
    main_w.show()
    sys.exit(app.Run())
