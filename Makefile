# Makefile for LiteLLM MCP Server

# Variables
BINARY_NAME=litellm-mcp-server
DOCKER_IMAGE=litellm-mcp-server:latest
KIND_CLUSTER=homelab

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Run the server locally
	@echo "Running $(BINARY_NAME) locally..."
	uv sync --locked --no-dev --no-editable
	uv run python ./src/litellm_mcp_server/mcp_server.py

.PHONY: docker-build
docker-build: ## Build the Docker image
	@echo "Building Docker image $(DOCKER_IMAGE)..."
	docker build -t $(DOCKER_IMAGE) .
	@echo "✅ Docker image built: $(DOCKER_IMAGE)"

.PHONY: docker-run
docker-run: ## Run the Docker image (port 8000)
	@echo "Running Docker image $(DOCKER_IMAGE)..."
	@docker run -p 8000:8000 -p 9090:9090 -e LITELLM_BASE_URL=http:\/\/localhost:8081 -e LITELLM_API_KEY="ThisIsAFakeKey" $(DOCKER_IMAGE)

.PHONY: deploy
deploy: docker-build ## Build and deploy to KIND cluster
	@echo "Loading image into KIND cluster $(KIND_CLUSTER)..."
	kind load docker-image $(DOCKER_IMAGE) --name $(KIND_CLUSTER)
	@echo "Deploying to Kubernetes..."
	kubectl apply -f kube/
	@echo "✅ Deployed to KIND cluster"
