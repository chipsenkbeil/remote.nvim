.PHONY: _install all deps dev-deps install uninstall update test

################################################################################
# BINARIES
################################################################################
FLAKE8=flake8
MYPY=mypy
NEOVIM=nvim
PIP=pip3
PYTEST=pytest
PYTEST_COV=py.test --cov=$(NVIM_PLUGIN_NAME)
THEMIS=./vim-themis/bin/themis
VINT=vint

################################################################################
# PATHS
################################################################################
DEPS_BASE=deps
NVIM_CONFIG=$(abspath $(HOME)/.config/nvim)
NVIM_CONFIG_PYTHON3_PLUGINS=$(abspath $(NVIM_CONFIG)/$(NVIM_PYTHON3_PLUGINS_BASE))
NVIM_PYTHON3_PLUGINS_BASE=rplugin/python3
PYTHON_DEV_REQUIREMENTS_FILE=$(DEPS_BASE)/dev-requirements.txt
PYTHON_REQUIREMENTS_FILE=$(DEPS_BASE)/requirements.txt

SRC_PYTHON3_PLUGIN=$(abspath $(NVIM_PYTHON3_PLUGINS_BASE)/$(NVIM_PLUGIN_NAME))
DST_PYTHON3_PLUGIN=$(abspath $(NVIM_CONFIG_PYTHON3_PLUGINS)/$(NVIM_PLUGIN_NAME))

################################################################################
# NAMES
################################################################################
NVIM_PLUGIN_NAME=remote

################################################################################
# THEMIS CONFIG
################################################################################
export THEMIS_VIM := $(NEOVIM)
export THEMIS_ARGS := -e -s --headless
export THEMIS_HOME := ./vim-themis

################################################################################
# RULES
################################################################################
all: deps install

deps:
	@$(PIP) install -r "$(PYTHON_REQUIREMENTS_FILE)"

dev-deps:
	@$(PIP) install -r "$(PYTHON_DEV_REQUIREMENTS_FILE)"

lint:
	$(VINT) --version
	$(VINT) plugin
	$(VINT) autoload
	$(FLAKE8) --version
	$(FLAKE8) $(SRC_PYTHON3_PLUGIN)
	$(MYPY) --version
	$(MYPY) --silent-imports $(SRC_PYTHON3_PLUGIN)

install: _install update
_install:
	@mkdir -p "$(NVIM_CONFIG_PYTHON3_PLUGINS)" && \
		ln -fs "$(SRC_PYTHON3_PLUGIN)" "$(DST_PYTHON3_PLUGIN)"
	$(info Installed $(SRC_PYTHON3_PLUGIN) to $(DST_PYTHON3_PLUGIN))

uninstall:
	@rm "$(DST_PYTHON3_PLUGIN)"
	$(info Removed symlink $(DST_PYTHON3_PLUGIN))

update:
	@$(NEOVIM) +UpdateRemotePlugins +qa
	@echo "Finished updating remote plugins!"

test:
	#$(THEMIS) --version
	#$(THEMIS) test/autoload/*
	$(PYTEST) --version
	$(PYTEST)
	$(PYTEST_COV) test/

vim-themis:
	@git clone https://github.com/thinca/vim-themis vim-themis

