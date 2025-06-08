.PHONY: help build up down restart logs shell test clean migrate upgrade

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Construir los contenedores
	docker compose build --no-cache

up: ## Levantar los servicios
	docker compose up -d

down: ## Detener los servicios
	docker compose down

restart: ## Reiniciar los servicios
	docker compose down && docker compose up -d

logs: ## Ver logs de los servicios
	docker compose logs -f

# Development commands
install: ## Instalar dependencias de desarrollo
	pip install -r requirements.txt
	pre-commit install
	pip install commitizen

setup: ## Configurar entorno de desarrollo completo
	pip install -r requirements.txt
	pre-commit install
	pip install commitizen
	@echo "Entorno de desarrollo configurado correctamente"

# Code quality commands
lint: ## Ejecutar linters
	flake8 app/ --max-line-length=88 --extend-ignore=E203,W503
	black --check app/
	isort --check-only app/

format: ## Formatear código
	black app/
	isort app/ --profile black

security: ## Análisis de seguridad
	bandit -r app/
	safety check

pre-commit: ## Ejecutar pre-commit en todos los archivos
	pre-commit run --all-files

# Git automation commands
commit: ## Commit automatizado con conventional commits
	@./scripts/git-auto.sh

cz-commit: ## Commit usando commitizen
	cz commit

release: ## Crear release manual
	cz bump --changelog

# CI/CD commands
ci-local: ## Simular CI localmente
	@echo "Ejecutando pipeline CI local..."
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) security
	@echo "Pipeline CI completado exitosamente"

# Deployment commands
deploy-staging: ## Deploy a staging
	@echo "Deploying to staging environment..."
	docker compose -f docker-compose.staging.yml up -d

deploy-prod: ## Deploy a producción
	@echo "Deploying to production environment..."
	@read -p "¿Estás seguro de que quieres hacer deploy a producción? [y/N]: " confirm && [ "$$confirm" = "y" ]
	docker compose -f docker-compose.prod.yml up -d

logs-web: ## Ver logs del servicio web
	docker compose logs -f web

logs-db: ## Ver logs de la base de datos
	docker compose logs -f db

shell: ## Acceder al shell del contenedor web
	docker compose exec web bash

db-shell: ## Acceder al shell de PostgreSQL
	docker compose exec db psql -U postgres -d fastapi_db

test: ## Ejecutar tests
	docker compose exec web python -m pytest

clean: ## Limpiar contenedores e imágenes
	docker compose down -v --rmi all

migrate: ## Crear nueva migración
	docker compose exec web alembic revision --autogenerate -m "$(msg)"

upgrade: ## Aplicar migraciones
	docker compose exec web alembic upgrade head

downgrade: ## Revertir migración
	docker compose exec web alembic downgrade -1

dev: ## Modo desarrollo completo
	make build && make up && make logs

reset: ## Reset completo del proyecto
	make down && docker system prune -f && make build && make up
