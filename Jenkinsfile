pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                git branch: 'main',
                    url: 'https://github.com/<ユーザー名>/aeb-jenkins-handson.git'
            }
        }
  
        stage('Lint') {
            steps {
                echo 'Running flake8...'
                powershell 'flake8 aeb_control.py test_aeb_control.py'
            }
        }
  
        stage('Test') {
            steps {
                echo 'Running pytest...'
                powershell 'pytest --junitxml=reports/test-results.xml'
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }
  
        stage('Package') {
            steps {
                echo 'Packaging artifacts...'
                powershell 'Compress-Archive -Path aeb_control.py -DestinationPath release.zip -Force'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'release.zip', followSymlinks: false
                }
            }
        }
    }
}