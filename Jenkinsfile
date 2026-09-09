pipeline {
    agent any

    environment {
        IMAGE_NAME     = "student-app"
        CONTAINER_NAME = "student-app-container"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build image') {
            steps { sh 'docker build -t $IMAGE_NAME .' }
        }

        stage('Stop old container') {
            steps { sh 'docker rm -f $CONTAINER_NAME || true' }
        }

        stage('Run new container') {
            steps {
                sh 'docker run -d --name $CONTAINER_NAME -p 5020:5000 $IMAGE_NAME'
            }
        }
    }
}
