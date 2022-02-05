##########################################################################################
#
#       | Software Application for Multipole Expansion and Spherical Harmonics |
#
#    INPUTS: data folder        -   contains data used
#            MainWindows folder -   contains Windows UI
#            utils folder       -   contains functions used
#
#    AUTHORS:             José Miguel, 95815
#                         Henry Machado, 95795
#                         Tomás Nunes, 95855
#
#    INITIAL CODING:        18/12/2021
#    LAST UPDATE:        03/02/2022
#
#    COURSE:        | Fenomenos Interactivos |
#
##########################################################################################

import os
import sys
import visvis as vv
from MainWindows.main_menu_ui import MainWindow

class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()
app = vv.use()
#app.create()
# Create Main Menu
main_w = MainWindow()
main_w.show()
sys.exit(app.Run())
