# =============================================================================
# FILE: __init__.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import neovim
from .client import RemoteClient
from .server import RemoteServer
from .utils import is_int, to_int
from . import logger


@neovim.plugin
class RemoteHandlers(logger.LoggingMixin):
    def __init__(self, nvim):
        self.nvim = nvim
        self.client = None
        self.server = None

        # TODO: Add logging variables to enable globally
        self.is_debug_enabled = True
        logger.setup(
            nvim,
            level='DEBUG',
            output_file='remote.log'
        )

    @neovim.command('RemoteSend', nargs='*', range='')
    def cmd_remote_send(self, args, range):
        if (self.client is not None):
            self.client.send(' '.join(args))
        if (self.server is not None):
            self.server.send(' '.join(args[1:]), args[0])

    @neovim.command('RemoteStop', nargs='*', range='')
    def cmd_remote_stop(self, args, range):
        if (self.client is not None):
            self.client.stop()
            self.client = None
        if (self.server is not None):
            self.server.stop()
            self.server = None

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

    @neovim.autocmd('BufWritePost',
                    pattern='*',
                    eval='expand("<afile>")',
                    sync=False)
    def on_bufwritepost(self, filename):
        self._on_fileupdate(filename)

    @neovim.autocmd('FilterWritePost',
                    pattern='*',
                    eval='expand("<afile>")',
                    sync=False)
    def on_filterwritepost(self, filename):
        self._on_fileupdate(filename)

    @neovim.autocmd('FileAppendPost',
                    pattern='*',
                    eval='expand("<afile>")',
                    sync=False)
    def on_fileappendpost(self, filename):
        self._on_fileupdate(filename)

    @neovim.autocmd('FileWritePost',
                    pattern='*',
                    eval='expand("<afile>")',
                    sync=False)
    def on_filewritepost(self, filename):
        self._on_fileupdate(filename)

    def _on_fileupdate(self, filename):
        """Kicks off a sync with the remote server to update the file.

        :param filename: The full path to the file relative to neovim
        """
        if (self.client is not None):
            m = UpdateFileStartRequestMessage(
                file_path=filename,
                file_version=1.0,
            )
            # TODO: Generate signature when creating packet
            p = m.to_packet().gen_signature(self.client.hmac)
            self.client.send(p.to_bytes())
        if (self.server is not None):
            self.server.send()
