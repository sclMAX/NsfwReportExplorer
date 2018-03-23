from ui_nsfw_scann import Ui_dlgNsfwScanner, QtCore, QtWidgets

class UiScanner(Ui_dlgNsfwScanner):
    
    def __init__(self, parent = None):
        self.ui = Ui_dlgNsfwScanner()
        self.ui.setupUi(parent)

