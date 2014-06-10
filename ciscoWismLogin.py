#!/usr/bin/python

import pexpect
import sys
import re
import getpass


# Passwords should never be in scripts
devicePass = getpass.getpass('Enter password: ')
if not devicePass:
    print "Must enter password"
    exit(-1)

# List of devices to connect to
controllers = ('128.252.18.18',)
    
# When using p.logfile write here
logfile = open('/tmp/cisco.log', 'w')

for controller in controllers:
    print "\n*** Working on controller: " + controller
    p = pexpect.spawn ('ssh ' + controller)
    p.logfile = sys.stdout
    #p.logfile = logfile

    # Login (non-standard ssh it prompts for user)
    p.expect ('User:')
    p.sendline ('nssuser')
    p.expect ('Password:')
    p.sendline (devicePass)
    p.expect ('>')

    # disable paging
    p.sendline ('config paging disable')
    p.expect('>')

    # get all aps
    p.sendline ('show ap summary')
    p.expect('>')

    for line in p.before.split('\r\n'):
    	#print 'DEBUG LINE: ', line

        found702w = re.match("^(.*)\s+\d\s+(AIR-CAP702W-A-K9).*$", line)
        if found702w:
            print ""
            print "******* -> Found 702 AP: ", found702w.group(1), found702w.group(2)
            print ""
            for i in range(1,5):
                #print 'RUNNING: config ap lan ' + str(i) +   ' enable AP18e7.2801.0170'
                p.sendline('config ap lan ' + str(i) +   ' enable ' + found702w.group(1) )
                p.expect ('>')
    
logfile.close()

