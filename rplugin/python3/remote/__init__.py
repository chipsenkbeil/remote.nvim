# =============================================================================
# FILE: __init__.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================

import neovim
from remote.client import RemoteClient
from remote.server import RemoteServer
from remote.utils import is_int, to_int

@neovim.plugin
class RemoteHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.client = None
        self.server = None

    @neovim.command('RemoteSend', nargs='*', range='')
    def cmd_remote_send(self, args, range):
        if (self.client is not None):
            self.client.send(' '.join(args))
        elif (self.server is not None):
            self.server.send(' '.join(args[1:]), args[0])

    @neovim.command('RemoteConnect', nargs='*', range='')
    def cmd_remote_connect(self, args, range):
        addr = '127.0.0.1'
        port = None
        key = ''

        length = len(args)
        if (length == 1):
            port = to_int(args[0])
        elif (length == 2 and is_int(args[0])):
            port = to_int(args[0])
            key = args[1]
        elif (length == 2 and is_int(args[1])):
            addr = args[0]
            port = to_int(args[1])
        elif (length == 3):
            addr = args[0]
            port = to_int(args[1])
            key = args[2]

        if (length < 1 or length > 3 or port is None):
            self.nvim.out_write('RemoteConnect [ADDR] <PORT> [KEY]\n')
            return

        self.nvim.out_write('Attempting to connect to {}:{}...\n'
                            .format(addr, port))
        self.client = RemoteClient(self.nvim, addr, port, key)
        self.client.run(lambda err: self.nvim.out_write(
            'Connected to {}:{}!\n'.format(addr, port)))

    @neovim.command('RemoteListen', nargs='*', range='')
    def cmd_remote_listen(self, args, range):
        addr = '127.0.0.1'
        port = None
        key = ''

        length = len(args)
        if (length == 1):
            port = to_int(args[0])
        elif (length == 2 and is_int(args[0])):
            port = to_int(args[0])
            key = args[1]
        elif (length == 2 and is_int(args[1])):
            addr = args[0]
            port = to_int(args[1])
        elif (length == 3):
            addr = args[0]
            port = to_int(args[1])
            key = args[2]

        if (length < 1 or length > 3 or port is None):
            self.nvim.out_write('RemoteListen [ADDR] <PORT> [KEY]\n')
            return

        self.nvim.out_write('Attempting to listen on {}:{}...\n'
                            .format(addr, port))
        self.server = RemoteServer(self.nvim, addr, port, key)
        self.server.run(lambda err: self.nvim.out_write(
            'Listening on {}:{}!\n'.format(addr, port)))

    @neovim.autocmd('BufWrite',
                    pattern='*',
                    eval='expand("<afile>")',
                    sync=False)
    def on_bufwrite(self, filename):
        self.nvim.out_write('Writing to ' + filename + "\n")
