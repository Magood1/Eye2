#import torch \\not supported yet
import tensorflow as tf
import numpy as np
import threading
from .singleton import Singleton

# Diagnoser (Singleton)
class Diagnoser(metaclass=Singleton):
    def __init__(self):
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def predict(self, left_image, right_image):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda model: model.diagnose(left_image, right_image), self.models))
        return results


# Model Loader Factory
class ModelLoaderFactory:
    loaders = {
        "h5": lambda path: tf.keras.models.load_model(path),
        "pb": lambda path: tf.saved_model.load(path),
        #"pt": lambda path: torch.jit.load(path) not supported yet please install 'torch' library
    }

    @staticmethod
    def get_loader(extension):
        loader = ModelLoaderFactory.loaders.get(extension.lower())
        if loader is None:
            raise ValueError(f"Unsupported model format: {extension}")
        return loader


# Eyes Model
class EyesModel:
    _model_cache = {}
    _cache_lock = threading.Lock()

    def __init__(self, model_path, strategy):
        self.model_path = model_path
        self.strategy = strategy
        self.model = self._load_model()

    def _load_model(self):
        with EyesModel._cache_lock:
            if self.model_path not in EyesModel._model_cache:
                extension = self.model_path.split('.')[-1]
                loader = ModelLoaderFactory.get_loader(extension)
                if loader:
                    EyesModel._model_cache[self.model_path] = loader(self.model_path)
            return EyesModel._model_cache[self.model_path]



    def diagnose(self, left_image, right_image):
        left_processed = self.strategy.apply(left_image)
        right_processed = self.strategy.apply(right_image)
        left_result = self.model.predict(np.expand_dims(left_processed, axis=0))[0]
        right_result = self.model.predict(np.expand_dims(right_processed, axis=0))[0]
        return left_result, right_result

    # Currently, EyesModel.diagnose() applies preprocessing before expanding the dimensions:
    # But some models expect normalized input, and preprocessing should match the model’s training input shape.

        """
    def diagnose(self, left_image, right_image):
        left_processed = self.strategy.apply(left_image)
        right_processed = self.strategy.apply(right_image)

        # Ensure correct input shape for model
        left_input = np.expand_dims(left_processed, axis=0).astype(np.float32)
        right_input = np.expand_dims(right_processed, axis=0).astype(np.float32)

        # Normalize images if needed (some models require 0-1 scaling)
        if np.max(left_input) > 1:
            left_input = left_input / 255.0
            right_input = right_input / 255.0

        left_result = self.model.predict(left_input)[0]
        right_result = self.model.predict(right_input)[0]
        return left_result, right_result

     # Ensure consistent input shape and normalization inside diagnose():
     #   ✔ Prevents incorrect model inputs.
     #   ✔ Handles different model expectations (raw vs. normalized images).


        """

