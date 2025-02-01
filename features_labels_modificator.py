from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
import numpy as np
import constants

class FeatureLabelModificator:
    def __init__(self, features, labels):
        """
        Initialize with features and labels.
        """
        self.__features = np.array(features)
        self.__labels = np.array(labels)
        self.__strategy = constants.FEATURE_LABEL_MODIFICATION_STRATEGY

    def modify(self):
            """
            Apply the selected modification strategy and return the result.
            """
            if self.__strategy == "class_weights":
                return self.__compute_class_weights()
            elif self.__strategy == "smote":
                return self.__apply_smote()
            elif self.__strategy == "map_labels":
                return self.__map_labels()
            else:
                raise ValueError(f"Unknown strategy: {self.__strategy}")
            
    def __compute_class_weights(self):
        """
        Compute class weights for labels.
        """
        classes = np.unique(self.__labels, axis=0)
        mapped_labels = self.__map_labels_to_classes(self.__labels)
        weights = compute_class_weight('balanced', classes=np.unique(mapped_labels), y=mapped_labels)
        return {i: weight for i, weight in enumerate(weights)}

    def __apply_smote(self):
        """
        Apply SMOTE to oversample the minority classes.
        """
        features_flat = self.__features.reshape(self.__features.shape[0], -1)
        mapped_labels = self.__map_labels_to_classes(self.__labels)
        smote = SMOTE(sampling_strategy="auto", random_state=42)
        features_resampled, labels_resampled = smote.fit_resample(features_flat, mapped_labels)
        features_resampled = features_resampled.reshape(-1, *self.__features.shape[1:])
        labels_resampled = self.__map_classes_to_labels(labels_resampled)
        return features_resampled, labels_resampled
    
    def __map_labels(self):
        """
        Map labels `[1, 1]` to `[0, 0]`.
        """
        mapped_labels = [
            [0, 0] if label == [1, 1] else label
            for label in self.__labels.tolist()
        ]
        return self.__features, np.array(mapped_labels)

    @staticmethod
    def __map_labels_to_classes(labels):
        """
        Map labels `[0, 0]`, `[1, 0]`, `[0, 1]`, `[1, 1]` to class IDs.
        """
        mapping = {
            (0, 0): 0,
            (1, 0): 1,
            (0, 1): 2,
            (1, 1): 3,
        }
        return np.array([mapping[tuple(label)] for label in labels])

    @staticmethod
    def __map_classes_to_labels(classes):
        """
        Map class IDs back to labels.
        """
        mapping = {
            0: [0, 0],
            1: [1, 0],
            2: [0, 1],
            3: [1, 1],
        }
        return np.array([mapping[c] for c in classes])