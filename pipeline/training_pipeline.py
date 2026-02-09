from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.training import ModelTraining
from utils.general_utils import load_config
from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


if __name__=="__main__":
    config = load_config('config.yaml')
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    processor = DataProcessor(config)
    processor.run()

    trainer = ModelTraining(config)
    trainer.run()