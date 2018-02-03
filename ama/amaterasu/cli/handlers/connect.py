"""
Connect to a remote machine via SSH. Upon connection, the bootstrap CLI will be uploaded to the remote machine and will live
as long as the session is alive.

Usage: ama connect [-p <port>] (-i <identity_file> [-s <passphrase>] | -u <username> -w <password>) <master_url>

Options:
    -h --help           Display this screen.
    -s --passphrase     If the supplied identity_file is locked by a passphrase, we will use the supplied passphrase.
    -p --port           Connect using this port. [default: 22]

"""

import os
import getpass
import paramiko

from .base import BaseHandler
from ..utils import interactive


class ConnectHandler(BaseHandler):

    def __init__(self, **args):
        super().__init__(**args)
        self.master_url = args['master_url']
        self.port = args['port']
        self.private_key = args['identity_file']
        self.user = args['username']
        self.password = args['password']
        self.passphrase = args['passphrase']

    def handle(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.private_key:
            client.connect(self.master_url, key_filename=os.path.abspath(self.private_key), passphrase=self.passphrase, port=self.port)
        else:
            username = self.user or input('Username: ')
            password = self.password or getpass.getpass()
            client.connect(self.master_url, username=username, password=password, port=self.port)
        sftp = client.open_sftp()
        sftp.chdir("/root")
        sftp.mkdir("amaterasu")
        # c = client.invoke_shell()
        # interactive.interactive_shell(c)
