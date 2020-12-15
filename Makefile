ifneq (,$(wildcard make_scripts/override_var.mk))
   include make_scripts/override_var.mk
endif


.DEFAULT_GOAL := help
SHELL_PYTHON:= $(shell which python)

DOCKER_PROJECT_NAME=ndlm_leak_monitoring_app
DOCKER_COMPOSE_ENV=docker/compose.env
DOCKER_COMPOSE_FILE=docker/docker-compose.yml

DOCKER:=docker --config docker
DOCKER_COMPOSE:=docker-compose -p $(DOCKER_PROJECT_NAME) --env-file  $(DOCKER_COMPOSE_ENV) -f $(DOCKER_COMPOSE_FILE)

miscellaneous_targets=format-py
export_targets=exports-py-deps exports-ufw-profile exports-static-files
docker_targets=docker-compose-up docker-compose-down
.PHONY: .FORCE_UPDATE $(miscellaneous_targets) $(export_targets) $(docker_targets)
.FORCE_UPDATE:

# reference: https://gist.github.com/prwhite/8168133#gistcomment-2749866
help:
	@printf "Usage\n";
	@awk '{ \
			if ($$0 ~ /^.PHONY: [a-zA-Z\-\_0-9]+$$/) { \
				helpCommand = substr($$0, index($$0, ":") + 2); \
				if (helpMessage) { \
					printf "\033[36m%-20s\033[0m %s\n", \
						helpCommand, helpMessage; \
					helpMessage = ""; \
				} \
			} else if ($$0 ~ /^[a-zA-Z\-\_0-9.]+:/) { \
				helpCommand = substr($$0, 0, index($$0, ":")); \
				if (helpMessage) { \
					printf "\033[36m%-20s\033[0m %s\n", \
						helpCommand, helpMessage; \
					helpMessage = ""; \
				} \
			} else if ($$0 ~ /^##/) { \
				if (helpMessage) { \
					helpMessage = helpMessage"\n                     "substr($$0, 3); \
				} else { \
					helpMessage = substr($$0, 3); \
				} \
			} else { \
				if (helpMessage) { \
					print "\n                     "helpMessage"\n" \
				} \
				helpMessage = ""; \
			} \
		}' \
		$(MAKEFILE_LIST)

## ===== Miscellaneous =====

## Formattin Python scripts by Black.
format-py:
	@black .

## ===== Exports ===== 

## Exports `tool.poetry.dependencies` to `requirements.txt`
exports-py-deps:
	@$(SHELL_PYTHON) -B -u scripts/dump_deps.py py

## Exports the application profile of UFW, copy to `/etc/ufw/applications.d`
exports-ufw-profile:
	@$(SHELL_PYTHON) -B -u scripts/dump_deps.py ufw_profile
	@echo "Copy to '/etc/ufw/applications.d'" && sudo cp "config/ufw/ndlm_leak_monitoring_app" "/etc/ufw/applications.d"

## Exports static files form Node.js modules
exports-static-files:
	@$(SHELL_PYTHON) -B -u scripts/dump_deps.py static_files

## ===== Docker =====
## Docker compose build
docker-compose-build:
	@$(DOCKER_COMPOSE) build
## Docker compose up
docker-compose-up:
	@$(DOCKER_COMPOSE) up -d

## Docker compose down
docker-compose-down:
	@$(DOCKER_COMPOSE) down

## Docker compose clean up
docker-compose-clean-up:
	@$(DOCKER_COMPOSE) down --rmi local  -v