#!/bin/bash

#-------------------------------------------
# $1 = User name
# $2 = Password
# $3 = Home directory
#-------------------------------------------

if [ "$#" -ne 3 ]; then
	echo "Illegal number of parameters"
	echo "Usage:"
	echo "   $0 <User name> <Password> <Home dir>"
	echo
	echo "Example:"
	echo "   ./add-ftp-account.sh user_name password user_home_dir"
	echo
	exit 1
fi

conf="conf/ftp.conf"
#perm="elrwm"
perm="wel"

#--CREATE NEW USER ACCOUNT
if [ -z "$( grep "name: $1" $conf )" ]; then
	echo "" >> $conf
	echo "  - name: $1" >> $conf
	echo "    dir: $3" >> $conf
	echo "    password: $2" >> $conf
	echo "    permission: $perm" >> $conf
	echo "Created new FTP account $1 having permission $perm"
else
	echo "The user $1 already exists: ABORT !!!"
	exit -1
fi

#--CREATE HOME DIR
if [ ! -d $3 ]; then
	mkdir $3
	chown www-data:www-data $3
	chmod -R g+w $3
	chmod g+s $3
	echo "Created new home dir: $3"
fi

#echo "HOMEs:"
#echo "$( ls -l $3/.. )"

#--RESTART easyftp DAEMON TO ENABLE NEW ACCOUNT
daemon_restart="zdaemon -C conf/zdaemon.conf restart"
read -p "Do you want to restart EASYFTP daemon now ? ('Yes' or 'No')" response
if [ "${response^^}" == "YES" ]; then
	$daemon_restart
else
	echo
	echo "ATTENTION:"
	echo "Remember to restart daemon manually to apply config changes:"
	echo "   $daemon_restart"
fi

echo "Done!"

