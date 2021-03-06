Easyftp
=======

A wrapper around pyftplib with start script and deps to run it as daemon.

On Debian/Ubuntu

    $ sudo apt-get install python-pip build-essential python-dev

Install the server

    $ sudo pip install -r requirements/common.txt
    $ cp conf/ftp-example.conf conf/ftp.conf

Now change your settings in the YAML file:

    users:
      - name: luca
        dir: /Users/luca
        password: test1
        permission: elradfmwM

      - name: test
        dir: /Users/luca/Development
        password: test2
        permission: elradfmwM

    server:
      port: 2121
      listen: 0.0.0.0
    #  Put your public ip here if you are behind a NAT (Amazon AWS or similar)
    #  masquerade_address: 8.8.8.8
      passive_ports:
        start: 60000
        end: 65535

Start the daemon:

     $ zdaemon -C conf/zdaemon.conf start

Autostart on boot:

    Edit /etc/rc.local and add a line to call the starter script: 'autostart-easyftp.sh'

To activate log rotation add this script in /etc/logrotate.conf:

    /var/log/pyftpd.log {
        daily
        compress
        rotate 10
        postrotate
            /usr/bin/pkill -xf "python app/main.py"
        endscript
    }

Enjoy!
