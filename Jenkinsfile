pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t jenkins-redis-demo:latest .'
            }
        }

        stage('Test App Container') {
            steps {
                sh '''
                docker rm -f redis-test app-test || true

                docker network create redis-demo-net || true

                docker run -d --name redis-test --network redis-demo-net redis:7

                docker run -d --name app-test \
                  --network redis-demo-net \
                  -e REDIS_HOST=redis-test \
                  -p 5000:5000 \
                  jenkins-redis-demo:latest

                sleep 5

                curl -f http://localhost:5000/health
                curl -f http://localhost:5000/
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                docker rm -f app-test redis-test || true
                docker network rm redis-demo-net || true
                '''
            }
        }
    }
}
