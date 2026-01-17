@Library('Shared') _
pipeline {
    agent any
    
    parameters {
        string(name: 'DOCKER_TAG', defaultValue: '', description: 'Docker tag of the image built by the CI job')
    }

    stages {
        stage("Workspace cleanup"){
            steps{
                script{
                    cleanWs()
                }
            }
        }
        
        stage('Git: Code Checkout') {
            steps {
                script{
                    clone("https://github.com/jayantmule03/City-Todo-App.git","main")
                }
            }
        }
        
        stage('Verify: Docker Image Tags') {
            steps {
                script{
                    echo "DOCKER TAG RECEIVED: ${params.DOCKER_TAG}"
                }
            }
        }
        
        
        stage("Update: Kubernetes manifest"){
            steps{
                script{
                    dir('kubernetes'){
                        sh """
                            sed -i -e s/City-Todo-Ap.*/City-Todo-App:${params.flask_DOCKER_TAG}/g flask.yaml
                        """
                    }
                }
            }
        }
  }
}
