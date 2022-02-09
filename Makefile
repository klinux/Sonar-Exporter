IMG="klinux/sonar-exporter"
NAME="sonar-exporter"
VERSION="1.0.1"
DEV="sonar-exporter-dev"

.PHONY: help
help:
	 @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / { printf "\033[36m%-30s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# DOCKER TASKS
image: ## Build the image and push
	docker build -t ${IMG}:${VERSION} -f Dockerfile .
	docker push ${IMG}:${VERSION}

dev: ## Using in developing mode
	docker build -t ${DEV} -f Dockerfile .
	docker-compose -f docker-compose.yaml up

stop: ## Stoping the developing mode
	docker-compose -f docker-compose.yaml down
