from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout

from ui.ui_component import DropZoneLabel, ResultsListWidget


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
        # UI betöltése a .ui fájlból
        uic.loadUi("ui/ui_window.ui", self.main_window)

        # UI elemek referenciáinak mentése
        old_drop_zone = self.main_window.findChild(QtWidgets.QLabel, "Drop_Zone")

        # Drop zóna lecserélése a saját DropZoneLabel osztályunkra
        self.drop_zone = DropZoneLabel(old_drop_zone.parent())
        self.drop_zone.setObjectName("Drop_Zone")
        self.drop_zone.setGeometry(old_drop_zone.geometry())

        # Kicseréljük a layout-ban
        layout = old_drop_zone.parent().layout()
        if layout:
            index = layout.indexOf(old_drop_zone)
            layout.removeWidget(old_drop_zone)
            layout.insertWidget(index, self.drop_zone)
        else:
            # Ha nincs layout, akkor pozíció alapján helyezzük el
            self.drop_zone.setParent(old_drop_zone.parent())
            self.drop_zone.move(old_drop_zone.pos())
            self.drop_zone.show()

        old_drop_zone.deleteLater()

        # Többi UI elem referenciájának mentése
        self.load_button = self.main_window.findChild(QtWidgets.QPushButton, "Load_Button")
        self.results_list = self.main_window.findChild(QtWidgets.QListWidget, "Object_List")

        return self

    # UI elemek összekapcsolása
    def connect_signals(self, controller):
        # Gombok összekapcsolása
        self.load_button.clicked.connect(controller.load_image)

        # Drop zóna összekapcsolása
        self.drop_zone.image_dropped.connect(controller.process_image)

        # Lista összekapcsolása
        self.results_list.itemSelectionChanged.connect(controller.highlight_selected_object)

        return self
