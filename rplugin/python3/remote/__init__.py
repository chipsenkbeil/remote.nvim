# =============================================================================
# FILE: __init__.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================

import neovim


@neovim.plugin
class RemoteHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('RemoteConnect', nargs='*', range='')
    def cmd_remote_connect(self, args, range):
        self.nvim.current.line = ('RemoteConnect with args: {}, range: {}'
                                  .format(args, range))

    @neovim.command('RemoteListen', nargs='*', range='')
    def cmd_remote_listen(self, args, range):
        self.nvim.current.line = ('RemoteListen with args: {}, range: {}'
                                  .format(args, range))

    @neovim.autocmd('BufWrite', pattern='*', eval='expand("<afile>")', sync=False)
    def on_bufwrite(self, filename):
        self.nvim.out_write('Writing to ' + filename)
