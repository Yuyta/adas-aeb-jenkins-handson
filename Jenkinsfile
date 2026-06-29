pipeline {
    agent any

    stages {
        stage('Lint') {
            steps {
                echo 'Running flake8...'
                sh 'flake8 aeb_control.py test_aeb_control.py'
            }
        }
  
        stage('Test') {
            steps {
                echo 'Running pytest...'
                sh 'pytest --junitxml=reports/test-results.xml'
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
                sh 'zip release.zip aeb_control.py'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'release.zip', followSymlinks: false
                }
            }
        }
    }
}
