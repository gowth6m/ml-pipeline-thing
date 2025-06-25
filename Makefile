# -------------------------------------------------------------------------------------------------
# Introspection targets
# -------------------------------------------------------------------------------------------------
SWAGGER_FILE_PATH ?= ./docs/openapi.json

.PHONY: help
help: targets

.PHONY: targets
targets:
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@echo "\033[34mAvailable Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'
	@echo ""

# -----------------------------------------------------------------------------------------------

.PHONY: cdk-deploy
cdk-deploy: ## Deploy the CDK stack
	cd infra/cdk && cdk deploy --all --require-approval never

.PHONY: cdk-destroy
cdk-destroy: ## Destroy the CDK stack
	cd infra/cdk && cdk destroy --all --require-approval never

# -----------------------------------------------------------------------------------------------
# VPS targets
# -----------------------------------------------------------------------------------------------

.PHONY: vps-up
vps-up: ## Start the VPS stack
	docker compose -f infra/docker/compose.vps.yml -p ml-pipeline-thing up -d --build

.PHONY: vps-down
vps-down: ## Stop the VPS stack
	docker compose -f infra/docker/compose.vps.yml -p ml-pipeline-thing down

.PHONY: create-ml-pipeline-thing-volumes
create-ml-pipeline-thing-volumes: ## Create docker volumes for ml-pipeline-thing
	@docker volume create ml-pipeline-thing-postgres-data
	@docker volume create ml-pipeline-thing-redis-data

.PHONY: gen-api-types
gen-api-types: ## Generate API types
	@npx swagger-typescript-api generate -p ${SWAGGER_FILE_PATH} -o ./frontend/src/types -n index.ts --no-client
