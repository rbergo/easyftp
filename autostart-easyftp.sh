#!/bin/bash

cwd=`pwd`
cd /home/admin/easyftp

zdaemon="/usr/local/bin/zdaemon"
$zdaemon -C conf/zdaemon.conf start
echo "EasyFTP status after boot -->" `$zdaemon -C conf/zdaemon.conf status` | logger

cd $cwd
