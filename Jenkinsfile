pipeline{
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    stages {
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning github repo to jenkins.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubtoken_1', url: 'https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git']])
                        }
                
                }
            }
        stage('Setting up our virtual env and installing dependencies'){
            steps{
                script{
                    echo 'Setting up our virtual env and installing dependencies.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubtoken_1', url: 'https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git']])
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                    }
                
                }
            }   
        }
    }
}