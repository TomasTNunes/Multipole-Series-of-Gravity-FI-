import os
os.environ['ETS_TOOLKIT'] = 'qt4'
import imp
try:
    imp.find_module('PySide') # test if PySide if available
except ImportError:
    os.environ['QT_API'] = 'pyqt' # signal to pyface that PyQt4 should be used
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from utils.Represent_SH_utils import *

#The actual visualization of Mayavi
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        self.scene.mlab.clf()
        self.scene.disable_render = False

    # Update Mayavi plot
    def update_plot(self,l,m,Type,Repres):
        # get coordinates of Spherical harmonic depending on type and representation
        # and module of Spherical Harmonic for surface color
        x, y, z, R = get_xyz(l,m,Type,Repres)
        self.scene.mlab.clf()
        # When m=0 there is no Imaginary representation
        if m == 0 and Type == 'Imag':
            pass
        else:
            # Update Mayavi mesh
            self.scene.mlab.mesh(x, y, z, scalars=R, colormap='jet')
            self.scene.mlab.view(-85,85)
    
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True)


# The QWidget containing the visualization, this is pure PyQt4 code.
# Mayavi Widget
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        #self.ui.setParent(self)


# Represent Spherical Harmonics Window Class
class Repres_SH_MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(555, 601)
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        #Central Widget
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        #GroupBox_DO
        self.groupBox_DO = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_DO.setObjectName("groupBox_DO")
        self.widget = QtWidgets.QWidget(self.groupBox_DO)
        self.widget.setGeometry(QtCore.QRect(20, 30, 91, 61))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        #ComboBox l degree
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        l_list = []
        [l_list.append(str(i)) for i in range(51)]
        self.comboBox.addItems(l_list)
        # Call l_change() function when new option of degree (l) selected
        self.comboBox.currentIndexChanged['QString'].connect(self.l_change)
        self.comboBox.setCurrentIndex(0)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        #ComboBox m order
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(['0'])
        # Call update_mayavi() function when new option of order (m) selected
        self.comboBox_2.currentIndexChanged['QString'].connect(self.update_mayavi)
        self.comboBox_2.setCurrentIndex(0)
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)

        #GroupBox Type
        self.groupBox_Type = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_Type.setObjectName("groupBox_Type")
        self.widget1 = QtWidgets.QWidget(self.groupBox_Type)
        self.widget1.setGeometry(QtCore.QRect(20, 30, 73, 65))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        #Radio Button Absolute
        self.radioButton = QtWidgets.QRadioButton(self.widget1)
        self.radioButton.setObjectName("radioButton")
        # Call update_mayavi() function when Absolute option is selected
        self.radioButton.clicked.connect(self.update_mayavi)
        self.verticalLayout.addWidget(self.radioButton)

        #Radio Button Real
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget1)
        self.radioButton_2.setObjectName("radioButton_2")
        # Call update_mayavi() function when Real option is selected
        self.radioButton_2.clicked.connect(self.update_mayavi)
        self.radioButton_2.setChecked(True)
        self.verticalLayout.addWidget(self.radioButton_2)

        #Radio Button Imag
        self.radioButton_3 = QtWidgets.QRadioButton(self.widget1)
        self.radioButton_3.setObjectName("radioButton_3")
        # Call update_mayavi() function when Imag option is selected
        self.radioButton_3.clicked.connect(self.update_mayavi)
        self.verticalLayout.addWidget(self.radioButton_3)

        #GroupBox Repres
        self.groupBox_Repres = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_Repres.setObjectName("groupBox_Repres")
        self.widget2 = QtWidgets.QWidget(self.groupBox_Repres)
        self.widget2.setGeometry(QtCore.QRect(20, 30, 81, 65))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #Radio Button Y_lm
        self.radioButton_4 = QtWidgets.QRadioButton(self.widget2)
        self.radioButton_4.setObjectName("radioButton_4")
        # Call update_mayavi() function when Y_lm option is selected
        self.radioButton_4.clicked.connect(self.update_mayavi)
        self.radioButton_4.setChecked(True)
        self.verticalLayout_2.addWidget(self.radioButton_4)

        #Radio Button Unit Sphere
        self.radioButton_5 = QtWidgets.QRadioButton(self.widget2)
        self.radioButton_5.setObjectName("radioButton_5")
        # Call update_mayavi() function when Unit Sphere option is selected
        self.radioButton_5.clicked.connect(self.update_mayavi)
        self.verticalLayout_2.addWidget(self.radioButton_5)

        #Radio Button Y_lm+1
        self.radioButton_6 = QtWidgets.QRadioButton(self.widget2)
        self.radioButton_6.setObjectName("radioButton_6")
        # Call update_mayavi() function when Y_lm+1 option is selected
        self.radioButton_6.clicked.connect(self.update_mayavi)
        self.verticalLayout_2.addWidget(self.radioButton_6)

        self.gridLayout_2.addWidget(self.splitter, 0, 1, 1, 1)

        #Mayavi Widget
        self.container1 = QtGui.QWidget()
        self.mayavi_widget = MayaviQWidget(self.container1)
        self.mayavi_widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mayavi_widget.setObjectName("mayavi_widget")
        self.update_mayavi()
        self.gridLayout_2.addWidget(self.mayavi_widget, 1, 1, 1, 1)

        #Spacers
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(1, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)

        self.retranslateUi()
        layout = QHBoxLayout()
        layout.addWidget(self.centralwidget)
        self.setLayout(layout)

        # Auxiliar Variables
        self.open = False
        self.exit = False

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Spherical Harmonics"))
        self.groupBox_DO.setTitle(_translate("MainWindow", "Degree and Order"))
        self.label.setText(_translate("MainWindow", "l"))
        self.label_2.setText(_translate("MainWindow", "m"))
        self.groupBox_Type.setTitle(_translate("MainWindow", "Type"))
        self.radioButton.setText(_translate("MainWindow", "Absolute"))
        self.radioButton_2.setText(_translate("MainWindow", "Real"))
        self.radioButton_3.setText(_translate("MainWindow", "Imaginary"))
        self.groupBox_Repres.setTitle(_translate("MainWindow", "Representation"))
        self.radioButton_4.setText(_translate("MainWindow", "Y_lm"))
        self.radioButton_5.setText(_translate("MainWindow", "Unit Sphere"))
        self.radioButton_6.setText(_translate("MainWindow", "(Y_lm + 1)"))
    
    # Updates order (m) combobox in function of the selected degree (l) and calls function update_mayavi()
    def l_change(self):
        if self.comboBox_2.count()-1 <= self.comboBox.currentIndex():
            current_m = self.comboBox_2.currentIndex()
            m_list = []
            [m_list.append(str(i)) for i in range(self.comboBox_2.count(),self.comboBox.currentIndex()+1)]
            self.comboBox_2.addItems(m_list)
        elif self.comboBox.currentIndex() < self.comboBox_2.currentIndex():
            self.comboBox_2.setCurrentIndex(self.comboBox.currentIndex())
            erase = self.comboBox_2.count()-1-self.comboBox.currentIndex()
            [self.comboBox_2.removeItem(self.comboBox.currentIndex()+1) for i in range(erase)]
        else:
            erase = self.comboBox_2.count()-1-self.comboBox.currentIndex()
            [self.comboBox_2.removeItem(self.comboBox.currentIndex()+1) for i in range(erase)]
        self.update_mayavi()

    # get the selected variables from the UI and calls update_plot() in the class Visualization()
    def update_mayavi(self):
        l = self.comboBox.currentIndex()
        m = self.comboBox_2.currentIndex()

        if self.radioButton.isChecked():
            Type = 'Abs'
        elif self.radioButton_2.isChecked():
            Type = 'Real'
        elif self.radioButton_3.isChecked():
            Type = 'Imag'

        if self.radioButton_4.isChecked():
            Repres = 'Y_lm'
        elif self.radioButton_5.isChecked():
            Repres = 'US'
        elif self.radioButton_6.isChecked():
            Repres = 'Y_lm+1'
        
        self.mayavi_widget.visualization.update_plot(l,m,Type,Repres)

    def closeEvent(self, event):
        if not self.exit:
            event.ignore()
            self.hide()
            self.open = False
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication([])
    main_w = Repres_SH_MainWindow()
    main_w.show()
    sys.exit(app.exec_())