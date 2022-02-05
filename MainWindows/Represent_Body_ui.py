import sys
import os
from pyface.qt import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication
import visvis as vv
from utils.Represent_body_utils import *

# Represent Body Surface Window Class
class Repres_BS_MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(1200, 850)
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        
        #Font
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.setFont(font)

        #Central Widget
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #Layouts
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(50)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(35)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #Group Box Body and Max Degree
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")

        #ComboBox body
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(60, 35, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox.setFont(font)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox.setObjectName("comboBox")
        self.body_comboBox_list_create()
        # Call update_body() function when new option of body is selected
        self.comboBox.currentIndexChanged['QString'].connect(self.update_body)

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 35, 41, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(220, 35, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #ComboBox lmax
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(305, 35, 61, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.lmax_comboBox_2_list_create()
        # Call update_lmax_2() function when new option of lmax is selected
        self.comboBox_2.currentIndexChanged['QString'].connect(self.update_lmax_2)

        self.horizontalLayout_2.addWidget(self.groupBox)

        #Group Box Add new lmax
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")

        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 35, 111, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        #Line Edit lmax
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(140, 35, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        #Button Calculate
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(240, 22, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        # Call Calculate_pressed() function when the button Calculate is pressed
        self.pushButton.clicked.connect(self.Calculate_pressed)

        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        #Label Calculating
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setHidden(True)
        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        #Visvis Widget 1
        self.fig1 = vv.backends.backend_pyqt5.Figure(self)
        self.horizontalLayout.addWidget(self.fig1._widget)

        #Visvis Widget 2
        self.fig1 = vv.backends.backend_pyqt5.Figure(self)
        self.horizontalLayout.addWidget(self.fig1._widget)

        #Visvis plot
        self.update_body()
        
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 700, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 110, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)

        self.retranslateUi()
        layout = QHBoxLayout()
        layout.addWidget(self.centralwidget)
        self.setLayout(layout)

        # Auxiliar Variables
        self.open = False
        self.exit = False

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Body Surface"))
        self.groupBox.setTitle(_translate("MainWindow", "Body and Max Degree"))
        self.label.setText(_translate("MainWindow", "Body"))
        self.label_2.setText(_translate("MainWindow", "Max Degree"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Add New Max Degree"))
        self.label_3.setText(_translate("MainWindow", "New Max Degree"))
        self.pushButton.setText(_translate("MainWindow", "Calculate"))
        self.label_4.setText(_translate("MainWindow", "CALCULATING...."))
    
    # Sets the list of the body combobox depending on the data available
    def body_comboBox_list_create(self):
        body_list = []
        path = './data/Repres_BS-data'
        files = os.listdir(path)
        [body_list.append(f) for f in files]
        self.comboBox.addItems(body_list)
        self.comboBox.setCurrentIndex(0)
    
    # Sets the list of the lmax combobox depending on the body selected and data available
    def lmax_comboBox_2_list_create(self):
        self.comboBox_2.clear()
        lmax_list = []
        body = self.comboBox.currentText()
        path = './data/Repres_BS-data/' + body
        files = os.listdir(path)
        for f in files:
            if f != f'{body}.OBJ':
                lmax = int(f.split('-')[1].lstrip('lmax').replace('.OBJ',''))
                lmax_list.append(lmax)
        lmax_list.sort()
        for i, item in enumerate(lmax_list):
            lmax_list[i] = str(item)
        if len(lmax_list) == 0:
            lmax_list.append('None')
        self.comboBox_2.addItems(lmax_list)
        self.comboBox_2.setCurrentIndex(0)
    
    # Updates or figure 1 or figure 2 of the visvis widget
    def update_visvis(self, figure, VERTICES, FACES):
        if figure == 1:
            self.figure1 = vv.figure(figure)
            vv.clf()
            vv.title(f"Original Body")
            vv.mesh(vertices=VERTICES, faces=FACES, verticesPerFace=3)
            self.a1 = vv.gca()
            self.a1.bgcolor = 'black'
            self.a1.axis.showGrid = False
            self.a1.axis.visible = False
            self.a1.camera = '3d'
            self.a1.camera.azimuth = 120
            self.a1.camera.elevation = 25
        elif figure == 2:
            self.figure2 = vv.figure(figure)
            vv.clf()
            if VERTICES is None and FACES is None:
                pass
            else:
                vv.title(f"SH l_m_a_x={self.comboBox_2.currentText()}")
                vv.mesh(vertices=VERTICES, faces=FACES, verticesPerFace=3)
                self.a2 = vv.gca()
                self.a2.bgcolor = 'black'
                self.a2.axis.showGrid = False
                self.a2.axis.visible = False
                self.a2.camera = self.a1.camera
    
    # calls function lmax_comboBox_2_list_create(), get_Vertices_Faces() [from Represent_body_utils], update_visvis() for figure 1 and update_lmax_1()
    def update_body(self):
        self.updating = 1
        self.lmax_comboBox_2_list_create()
        body = self.comboBox.currentText()
        # define Vertices and Faces of original body in class
        self.VERTICES, self.FACES = get_Vertices_Faces(body)
        self.update_visvis(1, self.VERTICES, self.FACES)
        self.update_lmax_1()
        self.updating = 0

    # Calls function update_visvis for figure 2 depending on body and lmax selected
    def update_lmax_1(self):
        body = self.comboBox.currentText()
        lmax = self.comboBox_2.currentText()
        if lmax == 'None':
            VERT_SH = None
            FACES = None
            self.update_visvis(2, VERT_SH, FACES)
        else:
            f = f'{body}-lmax{lmax}'
            VERT_SH, FACES = get_Vertices_Faces(f)
            self.update_visvis(2, VERT_SH, FACES)
    
    # Calls function update_visvis for figure 2 depending on body and lmax selected, if its not already updating that figure (self.updating == 0)
    def update_lmax_2(self):
        if self.updating == 0:
            body = self.comboBox.currentText()
            lmax = self.comboBox_2.currentText()
            if lmax == 'None':
                VERT_SH = None
                FACES = None
                self.update_visvis(2, VERT_SH, FACES)
            else:
                f = f'{body}-lmax{lmax}'
                VERT_SH, FACES = get_Vertices_Faces(f)
                self.update_visvis(2, VERT_SH, FACES)
        else:
            pass
    
    # calls function get_VERT_SH(), save_SH_file() and check_body_file_exists() [from Represent_body_utils]
    # calls function lmax_comboBox_2_list_create() and update_visvis() for figure 2
    # or calls function update_lmax_1()
    # depending on body and lmax selected
    def Calculate_pressed(self):
        body = self.comboBox.currentText()
        lmax = self.lineEdit.text()
        try:
            lmax = int(lmax)
            if not check_body_file_exists(lmax, body):
                QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                self.updating = 1
                VERTICES = self.VERTICES
                FACES = self.FACES
                VERT_SH = get_VERT_SH(VERTICES, lmax)
                save_SH_file(lmax, body, VERT_SH, FACES)
                self.lmax_comboBox_2_list_create()
                self.comboBox_2.setCurrentText(str(lmax))
                self.update_visvis(2, VERT_SH, FACES)   
                self.updating = 0
                QApplication.restoreOverrideCursor()
            else:
                self.comboBox_2.setCurrentText(str(lmax))
                self.update_lmax_1()
        except ValueError: pass    
    
    def closeEvent(self, event):
        if not self.exit:
            event.ignore()
            self.hide()
            self.open = False
        else:
            event.accept()

        
if __name__ == "__main__":
    app = vv.use()
    app.Create()
    main_w = Repres_BS_MainWindow()
    main_w.show()
    sys.exit(app.Run())
