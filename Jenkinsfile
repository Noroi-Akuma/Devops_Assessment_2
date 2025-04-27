pipeline {
    agent any

    environment {
        // Define your environment variables here (e.g., Python version)
        PYTHON_VERSION = "3.8"
        APP_VERSION = "1.0.0"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the source code from your repository
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Set up a Python virtual environment
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh './venv/bin/pip install fastapi uvicorn requests'
                }
            }
        }

        stage('Run FastAPI Application') {
            steps {
                script {
                    // Run FastAPI with Uvicorn in the background
                    sh 'nohup ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 80 &'
                    sleep 5 // Wait for the server to start
                }
            }
        }

        stage('Test API Endpoint') {
            steps {
                script {
                    // Send a request to the FastAPI root endpoint and check if the response is valid
                    def response = sh(script: 'curl -s http://localhost:80/', returnStdout: true).trim()
                    echo "Response: ${response}"

                    // Basic validation of the response
                    if (!response.contains('"message": "Hello from your DevOps Coursework 2 app!"')) {
                        error "API response validation failed!"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image if you're using Docker
                    sh 'docker build -t my-fastapi-app:${APP_VERSION} .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log into DockerHub (replace with your DockerHub credentials)
                    sh 'docker login -u noroi -p D@rk_L0rd@10'

                    // Push Docker image to DockerHub
                    sh 'docker push my-fastapi-app:${APP_VERSION}'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Clean up any running Docker containers (if you ran any)
                    sh 'docker ps -a -q | xargs docker rm -f || true'
                }
            }
        }
    }

    post {
        always {
            // Perform clean-up operations or post-build actions
            echo 'Build completed.'
        }
        success {
            echo 'The FastAPI app is successfully built, tested, and deployed!'
        }
        failure {
            echo 'Something went wrong in the pipeline.'
        }
    }
}
