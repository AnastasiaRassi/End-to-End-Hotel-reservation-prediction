# End-to-End Hotel Reservation Prediction

A complete machine learning pipeline for predicting hotel reservation cancellations, built with modular architecture and best practices for production-ready ML systems.

**Live Demo (Desktop Only)**: [http://alb-01-183381156.me-central-1.elb.amazonaws.com/](http://alb-01-183381156.me-central-1.elb.amazonaws.com/)

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Project Pipeline](#project-pipeline)
* [Configuration](#configuration)
* [Model Performance](#model-performance)
* [Contributing](#contributing)
* [Author](#author)
* [Acknowledgments](#acknowledgments)

---

## Overview

This project implements an end-to-end machine learning solution to predict hotel reservation cancellations. The system helps hotels optimize booking strategies, reduce revenue loss, and improve operational efficiency by forecasting which reservations are likely to be cancelled.

---

## Features

* **Modular Architecture**: Clean, maintainable code structure with separated components
* **Data Pipeline**: Automated data ingestion, validation, and transformation
* **Model Training**: Configurable pipeline with hyperparameter optimization
* **Model Evaluation**: Comprehensive metrics and reports
* **Artifact Management**: Version-controlled models and data artifacts
* **Configuration Management**: YAML-based configurations for easy experimentation
* **Logging & Monitoring**: Detailed logging for debugging and monitoring
* **Testing**: Unit tests for critical components
* **Web Deployment**: Flask app deployed on AWS Fargate, accessible publicly via ALB

---

## Project Structure

```
End-to-End-Hotel-reservation-prediction/
│
├── artifacts/                  # Stored models, preprocessors, and ML artifacts
├── custom_jenkins/             # Jenkins automation for CI/CD
│   └── Dockerfile              # Dockerfile for Jenkins pipeline
├── config.yaml                 # Main configuration file for the project
├── data/
│   ├── raw/                    # Raw hotel reservation datasets
│   └── processed/              # Preprocessed/cleaned datasets
├── notebook.ipynb              # Jupyter notebook for EDA and experimentation
├── src/                        # Source code for ML components
│   ├── data_ingestion.py       # Data ingestion scripts
│   ├── data_processing.py      # Data preprocessing scripts
│   └── training.py             # Model training scripts
├── logs/                       # Log files for debugging and monitoring
├── pipeline/                   
│   └── training_pipeline.py    # Training pipeline orchestration
├── tests/                      # Unit and integration tests
├── utils/                      # Helper functions and utilities
├── static/                     # Static files for the Flask web app
├── templates/                  # HTML templates for the Flask web app
├── requirements.txt            # Python dependencies
├── Jenkinsfile                 # Jenkins pipeline configuration
├── Dockerfile                  # Dockerfile for containerizing the project
├── setup.py                    # Python package setup script
└── README.md                   # Project documentation
```

---

## Installation

### Prerequisites

* Python 3.8 or higher
* pip package manager
* Virtual environment (recommended)

### Setup

```bash
git clone https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git
cd End-to-End-Hotel-reservation-prediction
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

---

## Usage

### Live Demo

* **Desktop only**: [http://alb-01-183381156.me-central-1.elb.amazonaws.com/](http://alb-01-183381156.me-central-1.elb.amazonaws.com/)

### Jupyter Notebooks

Explore `notebooks/` for:

* Exploratory Data Analysis (EDA)
* Feature engineering experiments
* Model comparison and evaluation
* Visualizations and insights

---

## Project Pipeline

1. **Data Ingestion**: Load raw data from S3 bucket, validate, and split into train/test sets
2. **Data Validation**: Check quality, schema, missing values, outliers
3. **Data Transformation**: Feature engineering, encoding, scaling, handling imbalanced data
4. **Model Training**: Train multiple ML algorithms, hyperparameter tuning, cross-validation
5. **Model Evaluation**: Accuracy, Precision, Recall, F1-Score, AUC-ROC, confusion matrix, feature importance
6. **Model Registry**: Save best-performing models with version control and artifact storage

---

## Configuration

YAML files in `config/` allow easy changes to:

* Data paths
* Model parameters
* Training settings
* Evaluation metrics
* Preprocessing steps

Example:

```yaml
data_ingestion:
  raw_data_path: data/raw/hotel_reservations.csv
  train_test_split_ratio: 0.8

model_training:
  algorithm: RandomForest
  hyperparameters:
    n_estimators: 100
    max_depth: 10
```

---

## Model Performance

Evaluated using:

* **Accuracy**: Overall prediction correctness
* **Precision**: Accuracy of positive predictions
* **Recall**: Coverage of actual positive cases
* **F1-Score**: Harmonic mean of precision and recall
* **AUC-ROC**: Class separation ability

Reports are saved in `artifacts/` after each training run.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**Anastasia Rassi**

* GitHub: [@AnastasiaRassi](https://github.com/AnastasiaRassi)

---

## Acknowledgments

* Hotel reservation dataset providers
* Open-source ML libraries (scikit-learn, pandas, numpy)
* ML community for best practices and inspiration

---

**Note**: This project is under active development. Live demo is **desktop only**.



