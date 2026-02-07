pipeline{
    agent any

    stages {
        stage{'Cloning github repo to jenkins'}{
            steps{
                script{
                    echo 'Cloning github repo to jenkins.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'githubtoken_1', url: 'https://github.com/AnastasiaRassi/End-to-End-Hotel-reservation-prediction.git']])
                }
            }
        }
    }
}