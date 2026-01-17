@Library('Shared') _
pipeline {
    agent any
    
    environment{
        SONAR_HOME = tool "Sonar"
    }
    
    parameters {
        string(name: 'DOCKER_TAG', defaultValue: '', description: 'Setting docker image for latest push')
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
        
        stage("Trivy: Filesystem scan"){
            steps{
                script{
                    trivyscan()
                }
            }
        }

        stage("OWASP: Dependency check"){
            steps{
                script{
                    owaspdependency()
                }
            }
        }
        
        stage("SonarQube: Code Analysis"){
            steps{
                script{
                    sonarqubeanalysis("Sonar","todo-app","todo-app")
                }
            }
        }
        
        stage("SonarQube: Code Quality Gates"){
            steps{
                script{
                    sonarqubecodequality()
                }
            }
        }

        stage("Docker: Build Images"){
            steps{
                script{
                    dockerbuild(
                          imageName: "jayantmule02/todo-app",
                            imageTag: params.DOCKER_TAG
                            )
                }
            }
        }
        
        stage("Docker: Push to DockerHub"){
            steps{
                script{
                    dockerpush(
                    imageName: "jayantmule02/todo-app",
                    imageTag: params.DOCKER_TAG,
                    credentials: "docker")
                }
            }
        }
    }
}
