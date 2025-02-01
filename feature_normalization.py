from sklearn.preprocessing import MinMaxScaler
import numpy as np

class FeatureNormalization:
    """
    Class that normalize all the features with the MinMax Scaler of Scikit:
    Takes as input the features calculated by the calculate_features_labels.py code.
    Runs at the end of features_labels calculations before saving.
    """
    def __init__(self, features):
        self.__features = features
        self.__minmax_scaler = MinMaxScaler()
        
    def run_normalization(self):
        self._convert_to_array()     # Convert to NumPy array
        self._debug_features()       # Inspect the feature array
        self._clean_features()       # Clean invalid values
        self._validate_cleaning()    # Validate cleaned features
        self.__fit()                 # Fit the scaler
        normalized_features = self.__transform()  # Transform the features
        return self._convert_to_tuples(normalized_features)

    def __fit(self):
        self.__minmax_scaler.fit(self.__features)

    def __transform(self):
        return self.__minmax_scaler.transform(self.__features)

    def _convert_to_array(self):
        self.__features = np.array([list(row) for row in self.__features], dtype=np.float64)

    def _debug_features(self):
        #print(f"Feature Shape: {self.__features.shape}")
        #print("Preview of Features:")
        #print(self.__features[:5])

        nan_mask = np.isnan(self.__features)
        inf_mask = np.isinf(self.__features)
        too_large_mask = np.abs(self.__features) > 1e10

        if nan_mask.any():
            print(f"NaN values found at indices: {np.argwhere(nan_mask)}")
        if inf_mask.any():
            print(f"Infinity values found at indices: {np.argwhere(inf_mask)}")
        if too_large_mask.any():
            print(f"Too large values found at indices: {np.argwhere(too_large_mask)}")

    def _clean_features(self):
        nan_mask = np.isnan(self.__features)
        inf_mask = np.isinf(self.__features)
        too_large_mask = np.abs(self.__features) > 1e10

        invalid_mask = nan_mask | inf_mask | too_large_mask

        if invalid_mask.any():
            print("Cleaning invalid values...")
            col_means = np.nanmean(self.__features, axis=0)
            for row, col in np.argwhere(invalid_mask):
                self.__features[row, col] = col_means[col]
        print("Invalid values cleaned.")

    def _validate_cleaning(self):
        if not np.isfinite(self.__features).all():
            raise ValueError("Features still contain invalid values after cleaning.")
        print("All features are valid.")

    def _convert_to_tuples(self, features):
        return [tuple(row) for row in features]
