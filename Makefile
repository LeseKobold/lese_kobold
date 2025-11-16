
build-requirements: ## Build the requirements.txt files
	poetry export -f requirements.txt --output requirements.txt --without-hashes

ruff: ## Run ruff
	poetry run ruff format . && \
	poetry run ruff check . --fix

run-dev-tests: ## Run pytests that are executed in the development CI/CD pipeline
	poetry run pytest -m "unit_test and not makes_api_call and not slow"

run-unit-tests: ## Run all unittests 
	poetry run pytest -m "unit_test"

adk-web:
	cd lesekobold/tests && \
	adk web

adk-cli:
	cd lesekobold/tests && \
	adk run test_agent

launch-api:
	uv run uvicorn lesekobold.src.main:app --app-dir src --host 0.0.0.0 --port 8000 --reload
