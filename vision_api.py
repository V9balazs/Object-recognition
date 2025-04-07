import io
import logging

from google.cloud import vision


class VisionAPI:
    """Google Cloud Vision API kezelő osztály"""

    def __init__(self):
        """Inicializálja a Vision API klienst"""
        try:
            self.client = vision.ImageAnnotatorClient()
            logging.info("Vision API kliens sikeresen inicializálva")
        except Exception as e:
            logging.error(f"Hiba a Vision API kliens inicializálásakor: {str(e)}")
            raise

    def detect_objects(self, image_path):
        """
        Objektumok felismerése a megadott képen

        Args:
            image_path (str): A kép elérési útja

        Returns:
            list: Felismert objektumok listája
        """
        logging.info(f"Objektumok felismerése: {image_path}")

        try:
            # Kép betöltése
            with io.open(image_path, "rb") as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            # API hívás
            response = self.client.object_localization(image=image)
            objects = response.localized_object_annotations

            # Eredmények feldolgozása
            results = []
            for obj in objects:
                results.append(
                    {
                        "name": obj.name,
                        "score": obj.score,
                        "bounding_box": {
                            "top_left": (
                                obj.bounding_poly.normalized_vertices[0].x,
                                obj.bounding_poly.normalized_vertices[0].y,
                            ),
                            "bottom_right": (
                                obj.bounding_poly.normalized_vertices[2].x,
                                obj.bounding_poly.normalized_vertices[2].y,
                            ),
                        },
                    }
                )

            # Hiba ellenőrzése
            if response.error.message:
                logging.error(f"Vision API hiba: {response.error.message}")
                raise Exception(f"{response.error.message}")

            logging.info(f"{len(results)} objektum felismerve")
            return results

        except Exception as e:
            logging.error(f"Hiba az objektumok felismerése közben: {str(e)}")
            raise
