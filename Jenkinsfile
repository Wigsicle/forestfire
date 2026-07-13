pipeline {
  agent any

  environment {
    IMAGE_NAME = "wigsicle/forestfire"
    KUBE_NAMESPACE = "apps"
    DEPLOYMENT_NAME = "forestfire-app"
    CONTAINER_NAME = "forestfire-app"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Get Git SHA') {
      steps {
        script {
          env.IMAGE_TAG = sh(
            script: "git rev-parse --short HEAD",
            returnStdout: true
          ).trim()
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh """
          docker build \
          --build-arg APP_VERSION=$IMAGE_TAG \
          -t $IMAGE_NAME:$IMAGE_TAG .
        """
      }
    }

    stage('Docker Login') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh """
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
          """
        }
      }
    }

    stage('Push Image (SHA)') {
      steps {
        sh """
          docker push $IMAGE_NAME:$IMAGE_TAG
        """
      }
    }

    stage('Tag Latest') {
      steps {
        sh """
          docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
          docker push $IMAGE_NAME:latest
        """
      }
    }

    stage('Update Deployment Manifest') {
    steps {
        sh """
        sed -i "s|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|" deployment.yaml
        """
    }
}

    stage('Commit Manifest') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'github-token',
            usernameVariable: 'GIT_USER',
            passwordVariable: 'GIT_TOKEN'
        )]) {
            sh """
                git config user.name "wigsicle"
                git config user.email "wigsicle@gmail.com"

                git add deployment.yaml

                if ! git diff --cached --quiet; then
                    git commit -m "ci: deploy ${IMAGE_TAG}"
                    git push https://${GIT_USER}:${GIT_TOKEN}@github.com/Wigsicle/forestfire.git HEAD:main
                else
                    echo "No deployment changes to commit."
                fi
            """
        }
    }
  }
  }

  post {
    success {
      echo "Deployment successful"
    }

    failure {
      echo "Deployment failed"
    }
  }
}