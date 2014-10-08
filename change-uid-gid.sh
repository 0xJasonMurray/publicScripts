#!/bin/bash

##
## Script to change the UID and GID of a user and their group.
## It changes the passwd, group, and all files.
##
## Manual restart of services are still required.
##


myUsername=$1
myOldUid=$2
myOldGid=$3
myNewUid=$4
myNewGid=$5

if [ $UID -ne 0 ]; then
	echo "Must run as root"
	exit -1
fi

if [ -z "$myUsername" -o -z "$myOldUid" -o -z "$myOldGid" -o -z "$myNewUid" -o -z "$myNewGid" ]; then
	echo "Syntax: $0 <username> <old uid> <old gid> <new uid> <new gid>"
	exit -1
fi


# This is a dangerous script, let the user know this!
echo "" 
echo "*** WARNING ***"
echo "You are about to change the user account: $myUsername from UID: $myOldUid to UID: $myNewUid"
echo "You are about to change the user account: $myUsername from GID: $myOldGid to GID: $myNewGid"
echo " "
echo "Press CTRL-C right now if this not what you want to do!"
echo "*** WARNING ***"
echo "" 
read OK

## Verify the user account exists
echo "" 
/bin/echo -n "Attempting to locate account: "
result=`grep "^$myUsername:" /etc/passwd`
if [ "$?" -eq 0 ]; then
	echo "Found: $result"
else
	echo "Not Found, exiting!"
	exit -1
fi
echo "" 

## Verify the group exists
echo "" 
/bin/echo -n "Attempting to locate group: "
result=`grep "^$myUsername:" /etc/group`
if [ "$?" -eq 0 ]; then
	echo "Found: $result"
else
	echo "Not Found, exiting!"
	exit -1
fi
echo "" 


# Let the user know what processes are running with this UID
result=`ps -ef | grep ^$myUsername`
if [ "$?" -eq 0 ]; then
	echo "" 
	echo "The following process are running under the OLD UID, you may have to manually restart them: "
	echo "$result"
	echo "" 
fi

# Find all the old files owned by old UID and change them.
result=`find / -uid $myOldUid -print 2> /dev/null`
echo "" 
echo "Found the following files with UID: $myOldUid: "
for i in $result; do
	echo "	$i"
done
/bin/echo -n "Are you sure you want to change them?  Press CTRL-C to exit now!"
read OK


/bin/echo -n "Changing files UID: "
for i in $result; do
	chown $myNewUid $i
done
echo "done."

echo "" 


# Find all the old files owned by old GID and change them.
result=`find / -gid $myOldGid -print 2> /dev/null`
echo "" 
echo "Found the following files with GID: $myOldGid: "
for i in $result; do
	echo "	$i"
done
/bin/echo -n "Are you sure you want to change them?  Press CTRL-C to exit now!"
read OK

/bin/echo -n "Changing files GID: "
for i in $result; do
	chgrp $myNewGid $i
done
echo "done."

# Group has to be changed before you can change the password file.
echo "" 
/bin/echo -n "Changing group: $myUsername from $myOldGid to $myNewGid: "
/usr/sbin/groupmod -g $myNewGid $myUsername
echo "done."
echo "" 



# Change the user account last in case the above fails
echo "" 
/bin/echo "Changing user: $myUsername from $myOldUid to $myNewUid: "
/usr/sbin/usermod -u $myNewUid -g $myNewGid $myUsername
echo "done."
echo "" 


