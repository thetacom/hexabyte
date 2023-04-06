.PHONY: clean lint bandit black check mypy pycodestyle ruff test build
PKG := hexabyte

SRC_DIR := $(PKG)
BUILD_DIR := dist
TEST_DIR := tests
DOCS_DIR := docs

build: .venv
	@echo "*****Packaging $(PKG)*****"
	@poetry build -n

.venv:
	@echo "*****Creating Python Virtual Environment*****"
	@poetry install -q -n

clean:
	@rm -rf $(BUILD_DIR) .mypy_cache .pytest_cache ./*/__pycache__ reports .coverage

check: .venv
	@echo "*****Pre-Commit Checks*****"
	@pre-commit run --all-files

lint: bandit black pylint mypy ruff pydocstyle pycodestyle

bandit: .venv
	@echo "*****Bandit*****"
	bandit -r --exit-zero $(SRC_DIR)

bandit_ci: .venv
	bandit -r -v -f xml -o reports/bandit.xml $(SRC_DIR)

black: .venv
	@echo "*****Black*****"
	@black --check $(SRC_DIR)

mypy: .venv
	@echo "*****Mypy*****"
	@mypy --pretty --disable-error-code import $(SRC_DIR)

pycodestyle: .venv
	@echo "*****Pycodestyle*****"
	@pycodestyle --max-line-length=80 $(SRC_DIR)

pydocstyle: .venv
	@echo "*****Pydocstyle*****"
	@pydocstyle $(SRC_DIR)

pylint: .venv
	@echo "*****Pylint*****"
	@pylint .

ruff: .venv
	@echo "*****Ruff*****"
	@ruff check --config pyproject.toml --show-source -e .

test: .venv
	@echo "*****Pytest*****"
	@pytest
