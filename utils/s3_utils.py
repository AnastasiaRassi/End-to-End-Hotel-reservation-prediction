import boto3
import sys
import os
from pathlib import Path
from loguru import logger
from utils.custom_exception import CustomException


class S3Progress:
    def __init__(self):
        self._seen_so_far = 0

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        mb = self._seen_so_far / (1024 * 1024)
        logger.info(f"Downloaded {mb:.2f} MB")


def load_s3_model(bucket_name, model_key, local_model_path):
    try:
        logger.info(f"Checking model in S3: s3://{bucket_name}/{model_key}")

        s3 = boto3.client("s3")

        # Check if object exists (avoids long waits + 404 later)
        try:
            s3.head_object(Bucket=bucket_name, Key=model_key)
            logger.info("Model found in S3")
        except Exception:
            raise CustomException(
                f"Model not found in S3 at key: {model_key}", sys
            )

        local_model_path = Path(local_model_path)
        local_model_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting download to {local_model_path}")

        # Download with progress
        s3.download_file(
            bucket_name,
            model_key,
            str(local_model_path),
            Callback=S3Progress()
        )

        logger.success(f"Model downloaded successfully to {local_model_path}")

        # Verify file size
        if not local_model_path.exists() or local_model_path.stat().st_size == 0:
            raise CustomException("Downloaded file is empty or missing", sys)

        return local_model_path

    except CustomException:
        raise
    except Exception as e:
        logger.exception("Error downloading model from S3")
        raise CustomException(e, sys)
