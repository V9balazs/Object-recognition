from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout
from ui_component import DropZoneLabel, ResultsListWidget


class UIManager:
    # UI elemek referenciái
    def __init__(self, main_window):
        self.main_window = main_window

        # UI elemek referenciái
        self.drop_zone = None
        self.load_button = None
        self.results_list = None

    # UI elemek beállítása
    def setup_ui(self):
        # Központi widget
        central_widget = QtWidgets.QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Fő layout
        main_layout = QVBoxLayout(central_widget)

        # UI elemek létrehozása a ui_window.ui alapján

        # Drop zóna
        self.drop_zone = DropZoneLabel()
        self.drop_zone.setObjectName("Drop_Zone")
        self.drop_zone.setGeometry(QtCore.QRect(10, 10, 531, 431))

        # Betöltés gomb
        self.load_button = QPushButton("Kép betöltése")
        self.load_button.setObjectName("Load_Button")
        self.load_button.setGeometry(QtCore.QRect(220, 460, 111, 51))

        # Objektum lista
        self.results_list = ResultsListWidget()
        self.results_list.setObjectName("Object_List")
        self.results_list.setGeometry(QtCore.QRect(560, 10, 256, 521))

        # Layout létrehozása a ui_window.ui elrendezése alapján
        content_layout = QHBoxLayout()

        # Bal oldali rész (drop zóna és gomb)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.drop_zone)
        left_layout.addWidget(self.load_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Elemek hozzáadása a content layout-hoz
        content_layout.addLayout(left_layout, 3)  # 3:1 arány
        content_layout.addWidget(self.results_list, 1)

        # Layout hozzáadása a fő layout-hoz
        main_layout.addLayout(content_layout)

        # Státuszsor beállítása
        self.main_window.statusBar().showMessage("Kész")

        # Ablak címének beállítása
        self.main_window.setWindowTitle("Object Recognition")

        # Ablak méretének beállítása
        self.main_window.resize(828, 550)

        return self

    def connect_signals(self, controller):
        """
        Összeköti az UI elemek jeleit a megfelelő eseménykezelőkkel

        Args:
            controller: Az alkalmazás vezérlője, amely tartalmazza az eseménykezelő függvényeket
        """
        # Gombok összekapcsolása
        self.load_button.clicked.connect(controller.load_image)

        # Drop zóna összekapcsolása
        self.drop_zone.image_dropped.connect(controller.process_image)

        # Lista összekapcsolása
        self.results_list.itemSelectionChanged.connect(controller.highlight_selected_object)

        return self
