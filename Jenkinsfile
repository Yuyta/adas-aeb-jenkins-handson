pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code has already been checked out by Pipeline script from SCM.'
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
