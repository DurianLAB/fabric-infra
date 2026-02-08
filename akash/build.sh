#!/bin/bash

# Build and push Docker image for Akash deployment

set -e

DOCKER_USER="${DOCKER_USER:-your-dockerhub-user}"
IMAGE_NAME="${IMAGE_NAME:-fabric-manager}"
TAG="${TAG:-latest}"

echo "Building Docker image..."
docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${TAG} .

echo ""
echo "Pushing to Docker Hub..."
docker push ${DOCKER_USER}/${IMAGE_NAME}:${TAG}

echo ""
echo "[OK] Image built and pushed: ${DOCKER_USER}/${IMAGE_NAME}:${TAG}"
echo ""
echo "Next steps:"
echo "1. Update deploy.yml with your Docker Hub username"
echo "2. Deploy to Akash: akash tx deployment create deploy.yml --from \$KEY_NAME"
