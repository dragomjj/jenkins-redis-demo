cat > Jenkinsfile <<'EOF'
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins-redis-demo'
        TEST_NETWORK = "jenkins-test-net-${BUILD_NUMBER}"
        REDIS_CONTAINER = "redis-test-${BUILD_NUMBER}"
        APP_CONTAINER = "app-test-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code already checked out by Jenkins SCM.'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Test App Container') {
            steps {
                sh '''
                    echo "Creating isolated Jenkins test network..."
                    docker network create ${TEST_NETWORK}

                    echo "Starting temporary Redis..."
                    docker run -d \
                      --name ${REDIS_CONTAINER} \
                      --network ${TEST_NETWORK} \
                      redis:7

                    echo "Starting temporary app container..."
                    docker run -d \
                      --name ${APP_CONTAINER} \
                      --network ${TEST_NETWORK} \
                      -e REDIS_HOST=${REDIS_CONTAINER} \
                      -e REDIS_PORT=6379 \
                      ${IMAGE_NAME}:latest

                    echo "Waiting for app..."
                    sleep 5

                    echo "Testing health endpoint..."
                    docker exec ${APP_CONTAINER} python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"

                    echo "Testing main endpoint..."
                    docker exec ${APP_CONTAINER} python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/').read().decode())"
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Cleaning Jenkins test containers and network..."
                docker rm -f ${APP_CONTAINER} ${REDIS_CONTAINER} || true
                docker network rm ${TEST_NETWORK} || true
            '''
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
EOF
