import logging

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QMessageBox


class DropZoneLabel(QtWidgets.QLabel):
    """
    Egyedi QLabel, amely támogatja a drag and drop funkcionalitást
    """

    # Egyedi jel a kép bedobásának jelzésére
    image_dropped = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        """Inicializálja a DropZoneLabel-t"""
        super().__init__(parent)
        self.setAcceptDrops(True)

        # Stílusok definiálása
        self.default_style = """
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f8f8f8;
            }
        """
        self.drag_over_style = """
            QLabel {
                border: 2px solid #66afe9;
                border-radius: 5px;
                background-color: #e6f2ff;
            }
        """
        self.setStyleSheet(self.default_style)

        # Alapértelmezett szöveg és beállítások
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Kezeli a drag enter eseményt"""
        if event.mimeData().hasUrls():
            self.setStyleSheet(self.drag_over_style)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """Kezeli a drag leave eseményt"""
        self.setStyleSheet(self.default_style)
        event.accept()

    def dragMoveEvent(self, event):
        """Kezeli a drag move eseményt"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Kezeli a drop eseményt"""
        self.setStyleSheet(self.default_style)

        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()

            # Ellenőrizzük, hogy a fájl kép-e
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                logging.info(f"Kép bedobva: {file_path}")
                self.image_dropped.emit(file_path)
            else:
                logging.warning(f"Nem támogatott fájltípus: {file_path}")
                QMessageBox.warning(self, "Nem támogatott fájl", "Csak képfájlokat lehet ide húzni.")

            event.acceptProposedAction()


class ResultsListWidget(QtWidgets.QListWidget):
    """
    Egyedi QListWidget a felismert objektumok megjelenítéséhez
    """

    def __init__(self, parent=None):
        """Inicializálja a ResultsListWidget-et"""
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
