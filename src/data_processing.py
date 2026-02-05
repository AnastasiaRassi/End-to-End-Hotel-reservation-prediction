import os
import sys
import pandas as pd
import numpy as np
from loguru import logger

from utils.custom_exception import CustomException
from utils.general_utils import load_config, load_data, RareCategoryGrouper, TopNEncoder, SkewHandler

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


class DataProcessor:
    def __init__(self, config):
        self.proc_config = config["data_processing"]
        self.ing_config = config["data_ingestion"]

        self.ing_train_path = self.ing_config["raw_train_file"]
        self.ing_test_path = self.ing_config["raw_test_file"]

        self.proc_train_path = self.proc_config["proc_train_file"]
        self.proc_test_path = self.proc_config["proc_test_file"]

        self.encoders = {} 


    def preprocess_data(self, df, is_train=True):
        try:
            logger.info("Starting data preprocessing")

            df = df.copy()

            df.drop(columns=["Booking_ID"], inplace=True, errors="ignore")
            df.drop_duplicates(inplace=True)

            cat_cols = self.proc_config["categorical_columns"]
            num_cols = self.proc_config["numerical_columns"]

            for col in cat_cols:
                if is_train:
                    encoder = LabelEncoder()
                    df[col] = encoder.fit_transform(df[col])
                    self.encoders[col] = encoder
                else:
                    df[col] = self.encoders[col].transform(df[col])

            logger.info("Handling skewness")
            skew_threshold = self.proc_config["skewness_threshold"]
            skewness = df[num_cols].skew()

            for col in skewness[skewness > skew_threshold].index:
                df[col] = np.log1p(df[col])

            return df

        except Exception as e:
            logger.exception("Error during preprocessing")
            raise CustomException("Preprocessing failed", e)


    def select_features(self, df):
        try:
            logger.info("Selecting top features")

            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = pd.DataFrame({
                "feature": X.columns,
                "importance": model.feature_importances_,
            }).sort_values(by="importance", ascending=False)

            k = self.proc_config["no_of_top_features"]
            selected_features = feature_importance["feature"].head(k).tolist()

            logger.info(f"Selected features: {selected_features}")

            return df[selected_features + ["booking_status"]]

        except Exception as e:
            logger.exception("Error during feature selection")
            raise CustomException("Feature selection failed", e)


    def save_data(self, df, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            logger.success(f"Saved data to {file_path}")

        except Exception as e:
            logger.exception("Error saving data")
            raise CustomException("Saving data failed", e)


    def run(self):
        try:
            logger.info("Starting data processing pipeline")

            train_df = self.preprocess_data(
                load_data(self.ing_train_path),
                is_train=True
            )

            test_df = self.preprocess_data(
                load_data(self.ing_test_path),
                is_train=False
            )

            train_df = self.balance_data(train_df)
            train_df = self.select_features(train_df)

            test_df = test_df[train_df.columns]

            self.save_data(train_df, self.proc_train_path)
            self.save_data(test_df, self.proc_test_path)

            logger.success("Data processing pipeline completed")

        except Exception as e:
            logger.exception("Pipeline failed")
            raise CustomException("Data processing pipeline failed", e)


if __name__ == "__main__":
    config = load_config("config/config.yaml")
    processor = DataProcessor(config)
    processor.run()
