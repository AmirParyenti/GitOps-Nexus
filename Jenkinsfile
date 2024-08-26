pipeline {
    agent {
        kubernetes {
            label "jenkins-agent"
            idleMinutes 5 // if the pod doesn't work 5 minutes the pod will fall downn
            yamlFile "build-pod.yaml"
            defaultContainer "ez-docker-helm-build"
        }
    }
    environment {
        GITLAB_CREDS = "gitlab"
        DOCKER_IMAGE = "amirparyenti/application_app"
        PROJECT_ID = "59011908"
        GITLAB_URL = "https://gitlab.com"
        IMAGE_VERSION = "v${BUILD_NUMBER}"
    }
    stages {
        stage("Checkout Code") {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml up -d'
                    sh 'docker-compose -f docker-compose.yaml run test pytest'
                    sh 'docker-compose -f docker-compose.yaml down'
                }
            }
        }
        stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'gitlab-api', variable: 'GITLAB_API_TOKEN')]) {
                        def response = sh(script: """
                        curl -s -o response.json -w "%{http_code}" --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/merge_requests" \
                        --form "source_branch=${env.BRANCH_NAME}" \
                        --form "target_branch=main" \
                        --form "title=MR from ${env.BRANCH_NAME} into main" \
                        --form "remove_source_branch=true"
                        """, returnStdout: true).trim()
                        if (response.startsWith("20")) {
                            echo "Merge request created successfully."
                        } else {
                            echo "Failed to create merge request. Response Code: ${response}"
                            def jsonResponse = readJSON file: 'response.json'
                            echo "Error message: ${jsonResponse.message}"
                            error "Merge request creation failed."
                        }
                    }
                }
            }
        }
        stage("Build Docker Image") {
            when {
                branch "main"
            }
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_VERSION}", "--no-cache .")
                }
            }
        }
        stage("Push Docker Image") {
            when {
                branch "main"
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        dockerImage.push("${IMAGE_VERSION}")
                    }
                }
            }
        }
        stage("Update Helm Chart") {
            when {
                branch "main"
            }
            steps {
                script {
                    sh "sed -i 's/tag:.*/tag: ${IMAGE_VERSION}/' ./data-app/values.yaml"
                }
            }
        }
        stage("Push Helm Chart to GitLab") {
            when {
                branch "main"
            }
            steps {
                script {
                    sh "git config --global --add safe.directory /home/jenkins/agent/workspace/GitOps_main"
                    sh "git config --global user.email 'amir29797@gmail.com'"
                    sh "git config --global user.name 'Amir CI'"
                    sh "git add ./data-app/values.yaml"
                    sh 'git commit -m "Update Helm chart values with new image version"'
                    withCredentials([string(credentialsId: 'gitlab-api', variable: 'GITLAB_API_TOKEN')]) {
                        sh 'git push -f https://gitlab-ci-token:${GITLAB_API_TOKEN}@gitlab.com/sela-tracks/1099/students/amirp/finalproject/finalproject/argodeploygitops.git HEAD:main'
                    }
                }
            }
        }
    }
}

        // stage("Check Last Commit Author") {
        //     steps {
        //         script {
        //             // Fetch the latest commit informationnn
        //             def authorName = sh(
        //                 script: "git log origin/main -1 --pretty=format:'%an'",
        //                 returnStdout: true
        //             ).trim()
        //             if (authorName == "Jenkins") {
        //                 currentBuild.result = 'SUCCESS'
        //                 error "Skipping build due to Jenkins commit"
        //             }
        //         }
        //     }
        // }
