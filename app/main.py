"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections.
"""

import os
import yaml
import logging
import pyftpdlib.log

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import path

this_dir = os.path.dirname(os.path.abspath(__file__))

def read_conf(config_file=os.path.join(this_dir, '../conf/ftp.conf')):
    conf_file = open(config_file, 'r')
    conf = yaml.safe_load(conf_file)
    return conf

class CustomHandler(FTPHandler):

    my_log = logging.getLogger('CustomHandler')

    def on_file_received(self, file):
        import os
        self.my_log.debug("Rename " + os.path.basename(file) + " to original file name")
        head, tail = list(path.split(file))[0], list(path.split(file))[1]
        os.rename(path.join(head, tail), path.join(head, tail[4:-1]))
        pass
    
    #Rob: it seems doesn't exist !     
    def on_incomplete_received(self, file):
        import os
        self.my_log.warn("on_incomplete_received('" + os.path.basename(file) + "')")
        os.remove(file)

    def ftp_STOR(self, file, mode='w'):
        import os
        self.my_log.debug("Rename " + os.path.basename(file) + " useing temp file name .in.xxx.")
        head, tail = list(path.split(file))[0], list(path.split(file))[1]
        file = path.join(head, ".in." + tail + ".")
        return FTPHandler.ftp_STOR(self, file, mode)

    def on_incomplete_file_received(self, file):
        import os
        self.my_log.warn("Remove partially uploaded file " + os.path.basename(file))
        # remove partially uploaded file
        #This happens on connection interrupted but not when Ctrl+C is pressed on FTP client (rob)
        os.remove(file)

    #Rob: added by me
    def on_incomplete_file_sent(self, file):
        import os
        self.my_log.warn("Remove partially downloaded file " + os.path.basename(file))
        # remove partially downloaded files
        os.remove(file)

def get_server(conf=None):

    print(conf)
    # Create users
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()
    for user in conf.get('users'):
        authorizer.add_user(user.get('name'), user.get('password'), user.get('dir'), perm=user.get('permission'))

    # TODO: implement anon user
    # authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = CustomHandler
    handler.authorizer = authorizer
    handler.log_prefix = '[%(username)s@%(remote_ip)s:%(remote_port)s]'
    
    # Define a customized banner (string returned when client connects)
    handler.banner = "simpleftp ready!"

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    server = conf.get('server', {})

    handler.masquerade_address = server.get('masquerade_address', None)
    range_start = min(server.get('passive_ports', {}).get('start', 60000), 65535)
    range_end = server.get('passive_ports', {}).get('end', max((range_start + 5000), 65535))
    # import pdb; pdb.set_trace()
    handler.passive_ports = range(range_start, range_end)

    address = (server.get('address', ''), server.get('port', '2121'))
    server = FTPServer(address, handler)
    pyftpdlib.log.LEVEL = log_level

    # set a limit for connections
    # server.max_cons = 256
    # server.max_cons_per_ip = 5

    # start ftp server
    # server.serve_forever()
    return server

if __name__ == '__main__':
    conf = read_conf()
    log_level = logging.DEBUG
    if conf.get('log').get('level').upper() == 'INFO':
        log_level = logging.INFO
    elif conf.get('log').get('level').upper() == 'WARN':
        log_level = logging.WARN
    elif conf.get('log').get('level').upper() == 'ERROR':
        log_level = logging.ERROR
   
    logging.basicConfig(level=log_level,
                    format='%(asctime)s %(levelname)-5s %(name)-13s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/var/log/pyftpd.log',
                    filemode='a')
    pyftpdlib.log.LEVEL = log_level

    server = get_server(conf)
    server.serve_forever()
