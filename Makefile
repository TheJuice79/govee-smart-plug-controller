# Makefile for Govee Smart Plug Controller

# Configuration
IMAGE_NAME=thejuice79/govee-smart-plug-controller
VERSION=1.2.1
PLATFORM=linux/amd64
DOCKER_DIR=./docker
DOCKERFILE=$(DOCKER_DIR)/Dockerfile

# Build the Docker image using Dockerfile in ./docker/
build:
	docker build --platform=$(PLATFORM) -f $(DOCKERFILE) -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

# Push both tags to Docker Hub
push:
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):latest

# Run all Python tests using local Python environment
test:
	PYTHONPATH=. pytest tests

# Build and push Docker image
publish: build push

# Clean up dangling Docker images
clean:
	docker image prune -f
