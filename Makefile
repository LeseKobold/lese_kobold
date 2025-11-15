
build-requirements: ## Build the requirements.txt files
	poetry export -f requirements.txt --output requirements.txt --without-hashes

ruff: ## Run ruff
	poetry run ruff format . && \
	poetry run ruff check . --fix

run-dev-tests: ## Run pytests that are executed in the development CI/CD pipeline
	poetry run pytest -m "unit_test and not makes_api_call and not slow"

run-unit-tests: ## Run all unittests 
	poetry run pytest -m "unit_test"
