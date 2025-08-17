.PHONY: format lint test fast-test coverage-report runner

PROJECT_PATH=.

isort:
	poetry run isort $(ISORT_ARGS) $(PROJECT_PATH)

black:
	poetry run black $(BLACK_ARGS) $(PROJECT_PATH)

lint: ISORT_ARGS = "--check" "--profile" "black"
lint: BLACK_ARGS = "--check" "--diff"
lint: isort black
	poetry run flake8 $(PROJECT_PATH)

format: isort black

test:
	@poetry run pytest -v --cov

fast-test:
	@poetry run pytest -v --cov -m "not slow"

coverage-report:
	@poetry run pytest --cov --cov-report=html