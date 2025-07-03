# Makefile for Govee Smart Plug Controller

# Configuration
VERSION=1.3.2
PLATFORM=linux/amd64
DOCKER_DIR=./docker
DOCKERFILE=$(DOCKER_DIR)/Dockerfile

# Registry tags
IMAGE_NAME_DOCKERHUB=thejuice79/govee-smart-plug-controller
IMAGE_NAME_GHCR=ghcr.io/thejuice79/govee-smart-plug-controller

# Build the Docker image
build:
	docker build --platform=$(PLATFORM) -f $(DOCKERFILE) -t $(IMAGE_NAME_DOCKERHUB):$(VERSION) -t $(IMAGE_NAME_DOCKERHUB):latest .

# Tag the image for GHCR
tag-ghcr:
	docker tag $(IMAGE_NAME_DOCKERHUB):$(VERSION) $(IMAGE_NAME_GHCR):$(VERSION)
	docker tag $(IMAGE_NAME_DOCKERHUB):latest $(IMAGE_NAME_GHCR):latest

# Push all tags to both registries
push:
	docker push $(IMAGE_NAME_DOCKERHUB):$(VERSION)
	docker push $(IMAGE_NAME_DOCKERHUB):latest
	docker push $(IMAGE_NAME_GHCR):$(VERSION)
	docker push $(IMAGE_NAME_GHCR):latest

# Run all Python tests
test:
	PYTHONPATH=. pytest tests

# Build and publish everything
publish: build tag-ghcr push

# Clean up
clean:
	docker image prune -f
