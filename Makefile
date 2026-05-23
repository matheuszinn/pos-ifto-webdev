# Makefile para o projeto Agenda Pro

.PHONY: help run test docker-build docker-run docker-clean install

help: ## Exibe esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências do projeto
	pip install -r requirements.txt

run: ## Roda o servidor de desenvolvimento
	export PYTHONPATH=$PYTHONPATH:. && export FLASK_APP="app:create_app()" && flask run --port 5001

test: ## Roda a suíte de testes (pytest)
	export PYTHONPATH=$PYTHONPATH:. && pytest

docker-build: ## Constrói a imagem Docker
	docker build -t pos-ifto-webdev .

docker-run: ## Roda o container Docker
	docker run -d -p 5001:5000 --name pos-ifto-container --env-file .env pos-ifto-webdev

docker-clean: ## Remove o container Docker
	docker stop pos-ifto-container || true
	docker rm pos-ifto-container || true

smoke-test: ## Executa o teste de fumaça (requer container rodando)
	python3 smoke_test.py
