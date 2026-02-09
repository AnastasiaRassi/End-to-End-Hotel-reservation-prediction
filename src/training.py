import os
import sys
from pathlib import Path
import boto3

import joblib
import pandas as pd
from loguru import logger

from utils.custom_exception import CustomException
from utils.general_utils import load_config, load_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

import optuna
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv

load_dotenv()


class ModelTraining:
    def __init__(self, config):
        self.config = config
        self.train_config = self.config["training"]
        self.proc_config = self.config["data_processing"]

        self.train_path = self.proc_config["proc_train_file"]
        self.test_path = self.proc_config["proc_test_file"]

        model_output_path = Path(self.train_config["model_output_path"])
        self.model_output_dir = model_output_path.parent
        self.model_name = model_output_path.name

    def _prepare_data(self):
        try:
            logger.info("Loading processed train and test data for model training")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns="booking_status")
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns="booking_status")
            y_test = test_df["booking_status"]

            logger.debug(
                f"Train shape: {X_train.shape}, Test shape: {X_test.shape}"
            )

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logger.exception("Error while preparing data for training")
            raise CustomException(e, sys)

    def _optimize_model(self, X_train, y_train, n_trials=25):
        try:
            logger.info(f"Starting Optuna hyperparameter search for RandomForest ({n_trials} trials)")

            def objective(trial):
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                    "max_depth": trial.suggest_int("max_depth", 10, 50),
                    "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
                    "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
                    "bootstrap": trial.suggest_categorical(
                        "bootstrap", [True, False]
                    ),
                    "random_state": 42,
                    "n_jobs": -1,
                }

                model = RandomForestClassifier(**params)
                score = cross_val_score(
                    model,
                    X_train,
                    y_train,
                    cv=5,
                    scoring="accuracy",
                    n_jobs=-1,
                ).mean()

                return score

            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=n_trials)

            logger.success(
                f"Best RF params: {study.best_params}, CV accuracy={study.best_value:.4f}"
            )

            return study.best_params

        except Exception as e:
            logger.exception("Error during hyperparameter optimization")
            raise CustomException(e, sys)

    def train_and_evaluate(self):
        try:
            X_train, X_test, y_train, y_test = self._prepare_data()

            best_params = self._optimize_model(X_train, y_train)

            logger.info("Training final RandomForest model with best parameters")
            model = RandomForestClassifier(**best_params)
            model.fit(X_train, y_train)

            with mlflow.start_run():
                mlflow.log_params(best_params)

                y_pred = model.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)

                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                mlflow.log_metric("f1", f1)

                logger.info(
                    f"Test metrics ‑ Accuracy: {accuracy:.4f}, "
                    f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}"
                )

                os.makedirs(self.model_output_dir, exist_ok=True)
                model_path = self.model_output_dir / self.model_name
                joblib.dump(model, model_path)
                logger.success(f"Saved trained model to {model_path}")

                s3 = boto3.client("s3")

                bucket_name = self.config["training"]["bucket_name"]
                s3_key = self.config["training"]["model_key"]
                s3.upload_file(str(model_path), bucket_name, s3_key)
                logger.success(f"Uploaded {model_path} to s3://{bucket_name}/{s3_key}")

                mlflow.sklearn.log_model(model, artifact_path="model")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "model_path": str(model_path),
            }

        except Exception as e:
            logger.exception("Error during model training / evaluation")
            raise CustomException(e, sys)

    def run(self):
        return self.train_and_evaluate()


if __name__ == "__main__":
    config = load_config("config.yaml")
    trainer = ModelTraining(config)
    trainer.run()
