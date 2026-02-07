pipeline {
    agent any

    environment {
        IMAGE_NAME = "hotel-res-mlops"
        AWS_REGION = "us-east-1"
        ECR_REPO = "123456789012.dkr.ecr.us-east-1.amazonaws.com/hotel-res-mlops"
    }

    stages {
        stage('Clone repo') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'githubtoken_1',
                        url: 'https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git'
                    ]]
                )
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-jenkins',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        sh """
                        # Login to ECR
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${ECR_REPO%/*}

                        # Build Docker image with caching
                        docker build --pull -t ${IMAGE_NAME}:latest .

                        # Tag for ECR
                        docker tag ${IMAGE_NAME}:latest ${ECR_REPO}:latest

                        # Push to ECR
                        docker push ${ECR_REPO}:latest
                        """
                    }
                }
            }
        }
        stage('Deploy to Amazon ECS') {
            withCredentials([usernamePassword(
                                credentialsId: 'aws-jenkins',
                                usernameVariable: 'AWS_ACCESS_KEY_ID',
                                passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                            )]) {
                                script {
                                    sh """
                                    # Login to ECR
                                    aws ecr get-login-password --region ${AWS_REGION} | \
                                    docker login --username AWS --password-stdin ${ECR_REPO%/*}

                                    # Build Docker image with caching
                                    docker build --pull -t ${IMAGE_NAME}:latest .

                                    # Tag for ECR
                                    docker tag ${IMAGE_NAME}:latest ${ECR_REPO}:latest

                                    # Push to ECR
                                    docker push ${ECR_REPO}:latest
                                    """
                                }
                            }
        }
    }
}
