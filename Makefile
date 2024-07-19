.PHONY: clean

PACKAGE_NAME=nitrokeyapp
PYTHON=python3
VENV=$(shell poetry env info --path)
VENV_BIN=$(VENV)/bin
VENV_PYTHON=$(VENV_BIN)/$(PYTHON)
#https://stackoverflow.com/questions/714100/os-detecting-makefile#12099167
ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    detected_OS := Windows
    $(error "Detected Windows $(detected_OS)")
else
    detected_OS := $(shell uname)  # same as "uname -s"
endif


ALL: init build

# setup environment
init: update-venv

update-venv:
ifeq (, $(shell which poetry))
$(error "No poetry in $(PATH)")
endif
	export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
	poetry env use $(PYTHON)
	poetry install --sync --without=deploy

# clean environment
semi-clean:
	rm -rf **/__pycache__
	rm -rf build/
	rm -rf dist/

clean: semi-clean
	rm -rf $(VENV)
	rm -rf .mypy_cache

# build
build:
	poetry build

build-pyinstaller-onefile:
	$(VENV_BIN)/pyinstaller ci-scripts/linux/pyinstaller/nitrokey-app-onefile.spec

build-pyinstaller-onedir:
	$(VENV_BIN)/pyinstaller ci-scripts/linux/pyinstaller/nitrokey-app-onedir.spec

# code checks
check-format:
	$(VENV_PYTHON) -m black --check $(PACKAGE_NAME)/

check-import-sorting:
	$(VENV_PYTHON) -m isort --check-only $(PACKAGE_NAME)/

check-style:
	$(VENV_PYTHON) -m flake8 $(PACKAGE_NAME)/

check-typing:
	$(VENV_PYTHON) -m mypy $(PACKAGE_NAME)/

check: check-format check-import-sorting check-style check-typing

fix:
	$(VENV_PYTHON) -m black $(PACKAGE_NAME)/
	$(VENV_PYTHON) -m isort $(PACKAGE_NAME)/
