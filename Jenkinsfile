pipeline {
    agent any

    environment {
        // Define variables
        PYTHON_VERSION = "3.8"
        APP_VERSION = "1.0.0"
        DOCKER_HUB_TOKEN = credentials('docker-hub-token')
        VAULT_PW = credentials('ansible_vault')
    }

    triggers {
        pollSCM('* * * * *') // Poll every minute
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', credentialsId: '<yourCredentialsId>', url: '<yourGitLink>'
                }
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

        stage('Docker Build and Push') {
            steps {
                script {
                    sh 'docker compose build'
                    sh 'docker tag <yourImageName> <yourDockerUsername>/<yourDockerRepoName>:latest'
                    sh "docker tag <yourImageName> <yourDockerUsername>/<yourDockerRepoName>:v1.${BUILD_NUMBER}"
                    sh "echo $DOCKER_HUB_TOKEN | docker login -u <yourDockerUsername> --password-stdin"
                    sh "docker push <yourDockerUsername>/<yourDockerRepoName>:v1.${BUILD_NUMBER}"
                    sh 'docker push <yourDockerUsername>/<yourDockerRepoName>:latest'
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                dir('ansible_files') {
                    sh 'cp /var/lib/jenkins/ec2_key.pem $WORKSPACE/ansible_files/ec2_key.pem'
                    sh 'chmod 600 $WORKSPACE/ansible_files/ec2_key.pem'
                    sh 'echo "$VAULT_PW"  | ansible-playbook --ask-vault-pass --extra-vars tag=v1.$BUILD_NUMBER deploy_application_to_staging_k8s.yaml'
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
