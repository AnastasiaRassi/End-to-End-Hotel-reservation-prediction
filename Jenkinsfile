pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        IMAGE_NAME = "jenkins-dind" 
        AWS_REGION = "me-central-1"       
        ECR_REPO = "123456789012.dkr.ecr.us-east-1.amazonaws.com/hotel-res-mlops" 
    }

    stages {
        stage('Cloning github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning github repo to Jenkins...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'githubtoken_1', 
                            url: 'https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up virtual env and installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual env and installing dependencies...'
                    sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install --default-timeout=100 --retries=10 -e .
                    """
                }
            }
        }

        stage('Building and pushing Docker image to ECR') {
            steps {
               withCredentials([usernamePassword(
                        credentialsId: 'aws-jenkins',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )])  {
                    script {
                        sh """
                        # Login to ECR
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${ECR_REPO%/*}

                        # Build Docker image
                        docker build -t ${IMAGE_NAME} .

                        # Tag image for ECR
                        docker tag ${IMAGE_NAME}:latest ${ECR_REPO}:latest

                        # Push to ECR
                        docker push ${ECR_REPO}:latest
                        """
                    }
                }
            }
        }
    }
