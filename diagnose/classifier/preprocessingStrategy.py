
import cv2
import numpy as np
from .singleton import Singleton

# Preprocessing Strategies (Singleton)
class PreprocessingStrategy(metaclass=Singleton):
    def apply(self, image):
        raise NotImplementedError("Subclasses must implement apply method.")

class CataractPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        image = cv2.resize(image, (224, 224))
        return cv2.convertScaleAbs(image, alpha=1.0, beta=50)

class DiabetesPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        image = cv2.resize(image, (224, 224))
        green_channel = image[:, :, 1]
        red_free_image = cv2.merge([green_channel, green_channel, green_channel])
        return cv2.convertScaleAbs(red_free_image, alpha=1.5, beta=50)

class GlaucomaPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        image = cv2.resize(image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0
        return image.astype(np.float32)

class HypertensionPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        image = cv2.resize(image, (224, 224))
        green_channel = image[:, :, 1]
        red_free_image = cv2.equalizeHist(green_channel)
        edges = cv2.Canny(red_free_image, 50, 150)
        blurred = cv2.GaussianBlur(red_free_image, (5, 5), 0)
        return np.stack([red_free_image, edges, blurred], axis=-1)

class PathologicalMyopiaPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        return cv2.resize(image, (224, 224))

class AgeIssuesPreprocessing(PreprocessingStrategy):
    def apply(self, image):
        image = cv2.resize(image, (224, 224))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(gray_image)
        image_faf = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)
        edges = cv2.Canny(image, 100, 200)
        return cv2.addWeighted(image, 0.8, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), 0.2, 0)
