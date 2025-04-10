import logging
import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QPushButton, QVBoxLayout

from ui.ui_manager import UIManager
from vision_api import VisionAPI

# Logging beállítása
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("object_detector.log"), logging.StreamHandler()],
)


class ObjectDetectorApp(QMainWindow):

    # Alkalmazás inicializálása
    def __init__(self):
        super().__init__()

        # Változók inicializálása
        self.image_path = None
        self.original_pixmap = None
        self.detected_objects = []

        try:
            # Vision API inicializálása
            self.vision_api = VisionAPI()

            # UI inicializálása külső menedzser segítségével
            self.ui_manager = UIManager(self)
            self.ui_manager.setup_ui().connect_signals(self)

            # UI elemek referenciáinak mentése a könnyebb hozzáférés érdekében
            self.drop_zone = self.ui_manager.drop_zone
            self.results_list = self.ui_manager.results_list

            logging.info("Alkalmazás sikeresen inicializálva")

        except Exception as e:
            logging.error(f"Hiba az alkalmazás inicializálásakor: {str(e)}")
            QMessageBox.critical(self, "Inicializálási hiba", f"Hiba történt az alkalmazás indításakor: {str(e)}")

    # Kép betöltése fájlválasztó dialógussal
    def load_image(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Kép kiválasztása", "", "Képek (*.png *.jpg *.jpeg *.bmp *.gif);;Minden fájl (*)"
            )

            if file_name:
                logging.info(f"Kép kiválasztva: {file_name}")
                self.process_image(file_name)
        except Exception as e:
            logging.error(f"Hiba a kép betöltése közben: {str(e)}")
            QMessageBox.critical(self, "Betöltési hiba", f"Hiba történt a kép betöltése közben: {str(e)}")

    # Kép feldolgozása
    def process_image(self, image_path):
        self.image_path = image_path
        self.original_pixmap = QPixmap(image_path)

        # Kép méretezése és megjelenítése
        self.display_image()

        # Objektumok felismerése
        try:
            # Státusz frissítése
            self.statusBar().showMessage("Objektumok felismerése folyamatban...")
            QtWidgets.QApplication.processEvents()  # UI frissítése

            # API hívás
            self.detected_objects = self.vision_api.detect_objects(image_path)

            # Eredmények megjelenítése
            self.update_results_list()

            # Státusz frissítése
            self.statusBar().showMessage(f"{len(self.detected_objects)} objektum felismerve", 3000)

        except Exception as e:
            logging.error(f"Hiba az objektumok felismerése közben: {str(e)}")
            QMessageBox.critical(self, "Hiba", f"Hiba történt az objektumok felismerése közben: {str(e)}")
            self.statusBar().showMessage("Hiba történt a feldolgozás során", 3000)

    # Kép megjelenítése
    def display_image(self, highlight_object=None):
        if self.original_pixmap is None:
            return

        # Kép másolása, hogy ne módosítsuk az eredetit
        pixmap = self.original_pixmap.copy()

        # Kép méretezése a címkéhez
        scaled_pixmap = pixmap.scaled(
            self.drop_zone.width(), self.drop_zone.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )

        # Ha van kijelölt objektum, rajzoljuk körbe
        if highlight_object is not None:
            painter = QPainter(scaled_pixmap)
            painter.setPen(QPen(QColor(255, 0, 0), 3))

            img_width = scaled_pixmap.width()
            img_height = scaled_pixmap.height()

            bbox = highlight_object["bounding_box"]
            x1 = int(bbox["top_left"][0] * img_width)
            y1 = int(bbox["top_left"][1] * img_height)
            x2 = int(bbox["bottom_right"][0] * img_width)
            y2 = int(bbox["bottom_right"][1] * img_height)

            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
            painter.end()

        # Kép megjelenítése
        self.drop_zone.setPixmap(scaled_pixmap)

    # Eredmények frissítése
    def update_results_list(self):
        self.results_list.clear()

        if not self.detected_objects:
            self.results_list.addItem("Nem találhatók objektumok")
            return

        # Objektumok rendezése a megbízhatóság szerint csökkenő sorrendben
        sorted_objects = sorted(self.detected_objects, key=lambda x: x["score"], reverse=True)

        for obj in sorted_objects:
            self.results_list.addItem(f"{obj['name']} ({obj['score']:.2f})")

    # Kiválasztott objektum kiemelése a képen
    def highlight_selected_object(self):
        selected_items = self.results_list.selectedItems()

        if not selected_items or not self.detected_objects:
            self.display_image()
            return

        selected_index = self.results_list.row(selected_items[0])

        # Ellenőrizzük, hogy a kiválasztott index érvényes-e
        if 0 <= selected_index < len(self.detected_objects):
            # Rendezzük az objektumokat a megbízhatóság szerint
            sorted_objects = sorted(self.detected_objects, key=lambda x: x["score"], reverse=True)
            selected_object = sorted_objects[selected_index]
            self.display_image(highlight_object=selected_object)


# Alkalmazás indítása
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ObjectDetectorApp()
    window.show()
    sys.exit(app.exec())
