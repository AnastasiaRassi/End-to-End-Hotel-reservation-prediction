# End-to-End Hotel Reservation Prediction

A complete machine learning pipeline for predicting hotel reservation cancellations, built with modular architecture and best practices for production-ready ML systems.

**Live Demo (Desktop Preferred)**: [http://alb-01-183381156.me-central-1.elb.amazonaws.com/](http://alb-01-183381156.me-central-1.elb.amazonaws.com/)

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Demo](#demo)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Project Pipeline](#project-pipeline)
* [Configuration](#configuration)
* [Model Performance](#model-performance)
* [Deployment](#deployment)
* [Contributing](#contributing)
* [Author](#author)
* [Acknowledgments](#acknowledgments)

---

## Overview

This project implements an end-to-end machine learning solution to predict hotel reservation cancellations. The system helps hotels optimize booking strategies, reduce revenue loss, and improve operational efficiency by forecasting which reservations are likely to be cancelled.

Hotel booking cancellations cost the hospitality industry billions annually. This predictive system provides actionable insights to help hotels better manage their inventory and reduce the financial impact of cancellations.

---

## Features

* **Modular Architecture**: Clean, maintainable code structure with separated components
* **Automated Data Pipeline**: S3-based data ingestion, validation, and transformation
* **Advanced Feature Engineering**: Custom scikit-learn transformers and feature selection
* **Model Training**: Random Forest classifier with hyperparameter tuning and cross-validation
* **Comprehensive Evaluation**: Precision, Recall, F1-Score metrics with detailed reports
* **Production Web Interface**: Flask REST API for real-time predictions
* **CI/CD Pipeline**: Jenkins automation for continuous integration and deployment
* **Containerization**: Docker for reproducible builds and deployments
* **Cloud Deployment**: AWS ECS (Fargate) with Application Load Balancer
* **Monitoring**: CloudWatch integration for logging and performance tracking
* **Artifact Management**: Version-controlled models and data artifacts
* **Configuration Management**: YAML-based configurations for easy experimentation

---

## Demo

![Hotel Reservation Prediction Demo](demo.gif)

*Enter booking details to receive real-time cancellation risk predictions!*

---

## Project Structure

```
End-to-End-Hotel-reservation-prediction/
│
├── artifacts/                      # Stored models, preprocessors, and ML artifacts
├── data/
│   ├── raw/                        # Raw hotel reservation datasets
│   └── processed/                  # Stores the train and test processed splits
├── src/                            # Source code for ML components
│   ├── data_ingestion.py           # Data ingestion scripts
│   ├── data_processing.py          # Data preprocessing and transformation
│   └── training.py                 # Model training scripts
├── pipeline/                       # Pipeline orchestration
│   └── training_pipeline.py        # Training pipeline execution
├── custom_jenkins/                 # CI/CD automation
│   └── Dockerfile                  # Jenkins pipeline Docker image
├── tests/                          # Unit and integration tests
├── utils/                          # Helper functions and utilities
├── notebook/                       # Jupyter notebook for EDA and experimentation
├── HOTEL_RES_PREDICTIONS.egg-info/ # Package metadata
├── application.py                  # Flask web application
├── config.yaml                     # Main configuration file for the project
├── Dockerfile                      # Container definition for deployment
├── Jenkinsfile                     # CI/CD pipeline configuration
├── .gitignore                      # Git ignore file
├── .gitattributes                  # Git attributes
├── .dockerignore                   # Docker ignore file
├── requirements.txt                # Python dependencies
├── setup.py                        # Python package setup script
└── README.md                       # Project documentation
```

---

## Installation

### Prerequisites

* Python 3.8 or higher
* pip package manager
* Docker (optional, for containerized deployment)
* AWS CLI (optional, for cloud deployment)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git
cd End-to-End-Hotel-reservation-prediction

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

### Docker Setup

```bash
# Build the Docker image
docker build -t hotel-reservation-prediction .

# Run the container
docker run -p 5000:5000 hotel-reservation-prediction
```

---

## Usage

### Running the Web Application Locally

```bash
# Start the Flask application
python application.py
```

Access the application at `http://localhost:5000`

### Training the Model

```bash
# Execute the complete training pipeline
python pipeline/training_pipeline.py
```

This will:
1. Ingest data from the configured source
2. Perform data validation and preprocessing
3. Train the model with optimal hyperparameters
4. Evaluate and save the best model
5. Generate performance reports in `artifacts/`

### Jupyter Notebooks

Explore the `notebook/` directory for:

* Exploratory Data Analysis (EDA)
* Feature engineering experiments
* Model comparison and evaluation
* Visualizations and statistical insights

---

## Project Pipeline

### 1. Data Ingestion
* Load raw data from Amazon S3 or local storage
* Perform initial data validation
* Split data into training and testing sets

### 2. Data Preprocessing
* Drop unnecessary columns and duplicates
* Group rare categories in categorical features
* Encode categorical variables (Top-N encoding and one-hot encoding)
* Correct skew in numerical features using log transforms
* Select top features based on RandomForest feature importance
* Save preprocessor and selected feature indices as artifacts for inference

### 3. Feature Selection
* Select features based on model importance scores
* Reduce dimensionality while maintaining predictive power

### 4. Model Training
* Train Random Forest classifier
* Hyperparameter tuning using GridSearchCV/RandomizedSearchCV
* K-fold cross-validation for robust evaluation

### 5. Model Evaluation
* Comprehensive metrics: Accuracy, Precision, Recall, F1-Score
* Confusion matrix analysis
* Feature importance visualization
* Model comparison reports

### 6. Model Deployment
* Save trained model and preprocessors as artifacts
* Version control for model tracking
* Integration with Flask API for real-time inference

---

## Configuration

All pipeline configurations are managed through `config.yaml`:

```yaml
data_ingestion:
  source_url: s3://your-bucket/hotel_reservations.csv
  raw_data_path: data/raw/hotel_reservations.csv
  train_test_split_ratio: 0.8

data_processing:
  description: |
    Configurable scikit-learn pipeline performing data cleaning, rare category grouping,
    encoding, skew correction, and feature selection using RandomForest importance.
    Fitted preprocessor and selected feature indices are saved as artifacts to ensure
    training–serving consistency. At inference, artifacts are loaded locally if available,
    otherwise automatically fetched from Amazon S3. All paths, columns, and parameters are
    controlled via config.yaml for reproducible, environment-independent deployment.

training:
  algorithm: RandomForest
  hyperparameters:
    n_estimators: 433
    max_depth: 43
    min_samples_leaf: 1
    bootstrap': False

Hyperparameter tuning done using Optuna.

evaluation:
  primary_metric: f1_score
  metrics:
    - accuracy
    - precision
    - recall
    - f1_score
```

Modify these settings to experiment with different configurations without changing code.

---

## Model Performance

The production model achieves the following performance metrics:

| Metric | Score |
|--------|-------|
| Accuracy | 90.19% |
| Precision | 87.46% |
| Recall | 81.77% |
| F1-Score | 84.52% |

### Key Features Influencing Predictions:
1. Lead time (days between booking and arrival)
2. Average price per room
3. Number of special requests
4. Market segment type
5. Number of weekend/weekday nights

Detailed evaluation reports and visualizations are saved in `artifacts/model_evaluation/` after each training run.

---

## Deployment

### AWS ECS (Fargate) Deployment

The application is deployed on AWS using a serverless container architecture:

**Architecture Components:**
* **Container**: Docker image hosted on Amazon ECR
* **Compute**: AWS ECS with Fargate (serverless)
* **Load Balancer**: Application Load Balancer for public access
* **Monitoring**: MLFlow for logs and metrics
* **CI/CD**: Jenkins pipeline for automated deployments

**Deployment Steps:**

```bash
# 1. Build and tag Docker image
docker build -t hotel-reservation-prediction:latest .

# 2. Tag for ECR
docker tag hotel-reservation-prediction:latest your-account.dkr.ecr.region.amazonaws.com/hotel-prediction:latest

# 3. Push to ECR
docker push your-account.dkr.ecr.region.amazonaws.com/hotel-prediction:latest

# 4. Update ECS service (automated via Jenkins)
# Jenkins pipeline handles deployment to ECS
```

### CI/CD Pipeline

The Jenkins pipeline (`Jenkinsfile`) automates:
1. Code checkout from repository
2. Docker image build
3. Unit and integration tests
4. Push to Amazon ECR
5. ECS service update
6. Health checks and rollback on failure

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

* Follow PEP 8 style guide for Python code
* Add unit tests for new features
* Update documentation for significant changes
* Ensure all tests pass before submitting PR

---

## Future Enhancements

- [ ] Production hardening with Gunicorn WSGI server
- [ ] Implement rate limiting for API endpoints
- [ ] Add model drift detection and monitoring
- [ ] A/B testing framework for model versions
- [ ] Real-time model retraining pipeline
- [ ] Extended feature engineering
- [ ] Integration with hotel booking systems
- [ ] Multi-model ensemble approach

---

## Author

**Anastasia Rassi**

* GitHub: [@AnastasiaRassi](https://github.com/AnastasiaRassi)
* LinkedIn: [Connect with me](www.linkedin.com/in/anastasia-al-rassi-9163a8264)

---

## Acknowledgments

* Hotel reservation dataset providers
* Open-source ML libraries: scikit-learn, pandas, numpy, Flask
* AWS for cloud infrastructure and deployment platform
* Jenkins community for CI/CD best practices
* ML and MLOps community for inspiration and guidance

---
**Note**: This project is under active development. The live demo is optimized for **desktop viewing only**.

For questions, issues, or suggestions, please open an issue on GitHub.


