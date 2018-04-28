.PHONY: _install all deps install uninstall update

################################################################################
# BINARIES
################################################################################
PIP=pip3
NEOVIM=nvim

################################################################################
# PATHS
################################################################################
NVIM_CONFIG=$(abspath $(HOME)/.config/nvim)
NVIM_CONFIG_PYTHON3_PLUGINS=$(abspath $(NVIM_CONFIG)/$(NVIM_PYTHON3_PLUGINS_BASE))
NVIM_PYTHON3_PLUGINS_BASE=rplugin/python3
PYTHON_REQUIREMENTS_FILE=requirements.txt

SRC_PYTHON3_PLUGIN=$(abspath $(NVIM_PYTHON3_PLUGINS_BASE)/$(NVIM_PLUGIN_NAME))
DST_PYTHON3_PLUGIN=$(abspath $(NVIM_CONFIG_PYTHON3_PLUGINS)/$(NVIM_PLUGIN_NAME))

################################################################################
# NAMES
################################################################################
NVIM_PLUGIN_NAME=remote

################################################################################
# RULES
################################################################################
all: deps install update

check:
	$(info $(NVIM_CONFIG))
	$(info $(NVIM_CONFIG_PYTHON3_PLUGINS))

deps:
	@$(PIP) install -r "$(PYTHON_REQUIREMENTS_FILE)"

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

