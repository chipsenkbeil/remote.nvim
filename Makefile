.PHONY: _install all deps dev-deps install uninstall update test

################################################################################
# BINARIES
################################################################################
PIP=pip3
NEOVIM=nvim

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
# THEMIS
################################################################################
PATH := ./vim-themis/bin:$(PATH)
export THEMIS_VIM := $(NEOVIM)
export THEMIS_ARGS := -e -s --headless
export THEMIS_HOME := ./vim-themis

################################################################################
# RULES
################################################################################
all: deps install update

deps:
	@$(PIP) install -r "$(PYTHON_REQUIREMENTS_FILE)"

dev-deps:
	@$(PIP) install -r "$(PYTHON_DEV_REQUIREMENTS_FILE)"

lint:
	vint --version
	vint plugin
	vint autoload
	flake8 --version
	flake8 rplugin/python3/remote
	mypy --version
	mypy --silent-imports rplugin/python3/remote

install: _install update
_install:
	@mkdir -p "$(NVIM_CONFIG_PYTHON3_PLUGINS)" && \
		ln -fs "$(SRC_PYTHON3_PLUGIN)" "$(DST_PYTHON3_PLUGIN)"
	$(info Installed $(SRC_PYTHON3_PLUGIN) to $(DST_PYTHON3_PLUGIN))

uninstall:
	@rm "$(DST_PYTHON3_PLUGIN)"

update:
	@$(NEOVIM) +UpdateRemotePlugins +qa
	@echo "Finished updating remote plugins!"

test:
	themis --version
	themis test/autoload/*
	pytest --version
	pytest

vim-themis:
	git clone https://github.com/thinca/vim-themis vim-themis

