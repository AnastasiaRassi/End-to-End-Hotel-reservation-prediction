import os
import sys
import pandas as pd
import numpy as np
from loguru import logger

from utils.custom_exception import CustomException
from utils.general_utils import load_config, load_data
from utils.processing_utils import RareCategoryGrouper, TopNEncoder, SkewHandler

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


class DataProcessor:
    def __init__(self, config):
        self.proc_config = config["data_processing"]
        self.ing_config = config["data_ingestion"]

        raw_data_dir = self.ing_config["raw_data_dir"]
        self.ing_train_path = os.path.join(raw_data_dir, "train_Hotel_Reservations.csv")
        self.ing_test_path = os.path.join(raw_data_dir, "test_Hotel_Reservations.csv")

        self.proc_train_path = self.proc_config["proc_train_file"]
        self.proc_test_path = self.proc_config["proc_test_file"]

        self.preprocessor = None

        self.rare_cols = ["market_segment_type", "room_type_reserved"]
        self.num_cols = self.proc_config["numerical_columns"]
        self.skew_threshold = self.proc_config.get("skewness_threshold", 1.0)

    def _prepare_data(self, df):
        df = df.copy()
        df.drop(columns=["Booking_ID"], inplace=True, errors="ignore")
        df.drop_duplicates(inplace=True)
        return df

    def _build_preprocessor(self):
        preprocessor = ColumnTransformer(
            [
                (
                    "rare_grouped",
                    Pipeline(
                        [
                            ("grouper", RareCategoryGrouper(threshold=500)),
                            (
                                "ohe",
                                OneHotEncoder(
                                    drop="first",
                                    handle_unknown="ignore",
                                    sparse_output=False,
                                ),
                            ),
                        ]
                    ),
                    self.rare_cols,
                ),
                ("meal", TopNEncoder(n=3, prefix="meal"), ["type_of_meal_plan"]),
                ("numeric", SkewHandler(skew_threshold=self.skew_threshold), self.num_cols),
            ]
        )
        return preprocessor

    def _transform_features(self, X_train, X_test, y_train):
        try:
            logger.info("Building and fitting ColumnTransformer preprocessor")

            self.preprocessor = self._build_preprocessor()

            self.preprocessor.fit(X_train, y_train)

            X_train_transformed = pd.DataFrame(self.preprocessor.transform(X_train))
            X_test_transformed = pd.DataFrame(self.preprocessor.transform(X_test))

            logger.info(
                f"Transformed features - Train: {X_train_transformed.shape}, Test: {X_test_transformed.shape}"
            )

            return X_train_transformed, X_test_transformed

        except Exception as e:
            logger.exception("Error during feature transformation")
            raise CustomException(e, sys)

    def _select_features(self, X_train, y_train, X_test):
        try:
            logger.info("Selecting top features using RandomForest feature importance")

            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)

            feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]

            feature_importance = (
                pd.DataFrame(
                    {
                        "feature": feature_names,
                        "importance": model.feature_importances_,
                    }
                )
                .sort_values(by="importance", ascending=False)
            )

            k = self.proc_config["no_of_top_features"]
            selected_indices = feature_importance.head(k).index.tolist()
            selected_features = feature_importance.head(k)["feature"].tolist()

            logger.info(f"Selected top {k} features: {selected_features}")

            X_train_selected = X_train.iloc[:, selected_indices]
            X_test_selected = X_test.iloc[:, selected_indices]

            return X_train_selected, X_test_selected

        except Exception as e:
            logger.exception("Error during feature selection")
            raise CustomException(e, sys)

    def save_data(self, df, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            logger.success(f"Saved data to {file_path}")

        except Exception as e:
            logger.exception("Error saving data")
            raise CustomException(e, sys)

    def run(self):
        try:
            logger.info("Starting data processing pipeline")

            train_df = load_data(self.ing_train_path)
            test_df = load_data(self.ing_test_path)

            logger.info(f"Loaded train: {train_df.shape}, test: {test_df.shape}")

            train_df = self._prepare_data(train_df)
            test_df = self._prepare_data(test_df)

            X_train = train_df.drop(columns="booking_status")
            y_train = train_df["booking_status"]
            X_test = test_df.drop(columns="booking_status")
            y_test = test_df["booking_status"]

            target_map = {"Not_Canceled": 0, "Canceled": 1}
            y_train = y_train.replace(target_map)
            y_test = y_test.replace(target_map)

            X_train_transformed, X_test_transformed = self._transform_features(
                X_train, X_test, y_train
            )

            X_train_selected, X_test_selected = self._select_features(
                X_train_transformed, y_train, X_test_transformed
            )

            train_processed = pd.concat(
                [X_train_selected, pd.Series(y_train, name="booking_status")], axis=1
            )
            test_processed = pd.concat(
                [X_test_selected, pd.Series(y_test, name="booking_status")], axis=1
            )

            self.save_data(train_processed, self.proc_train_path)
            self.save_data(test_processed, self.proc_test_path)

            logger.success("Data processing pipeline completed")

        except Exception as e:
            logger.exception("Data processing pipeline failed")
            raise CustomException(e, sys)


if __name__ == "__main__":
    config = load_config("config.yaml")
    processor = DataProcessor(config)
    processor.run()
