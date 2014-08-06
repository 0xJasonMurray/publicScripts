#!/usr/bin/python

'''
  It is not pretty, but it gets rid of our Meru APs and 
  configures our Cisco gear.
'''

import pexpect
import re
import getpass


# Global Variables
username = 'username-goes-here'
switch = 'switch.example.com'
vlan702 = 720 
vlanManagedAp = 345
devicePass = 'SuperSecurePassword'


# Passwords should never be in scripts
if not devicePass:
    devicePass = getpass.getpass('Enter password: ')

# List of devices to connect to
controllers = (username + '@' + switch,)
    
# When using p.logfile write here
logfile = open('/tmp/cisco.log', 'w')

prevLine = None


def setOptions(apType):
  if int(apType) == 70:
    print "  power inline consumption 15399"
    print "  switch access vlan", vlan702
    print "  speed auto"
    print "  duplex auto"

  if int(apType) == 37:
    print "  switch access vlan", vlanManagedAp
    print "  speed auto"
    print "  duplex auto"

for controller in controllers:
    print "\n*** Working on controller: " + controller
    p = pexpect.spawn ('ssh ' + controller)
    #p.logfile = sys.stdout
    p.logfile = logfile

    # Login (non-standard ssh it prompts for user)
    p.expect ('word:')
    p.sendline (devicePass)
    p.expect ('#')

    # get all aps
    p.sendline ('term len 0')
    p.expect('#')

    # get all aps
    p.sendline ('show cdp neigh')
    p.expect('#')

    print ""
    for line in p.before.split('\r\n'):
    	print '! Sanity Check: ', line

	nameOnly = re.match("^([A-Z0-9a-z-]+).\w+.wustl.edu$", line)
	if nameOnly:
		prevLine = nameOnly.group(1)
		#print "Prev line: {0}".format(nameOnly.group(1))

	if prevLine:
		nextLine = re.match("^\s+(\w+\s+[\d/]+).*AIR-CAP(\d+)", line)
		if nextLine: 
			#print "Found next line: {0} {1}".format(nextLine.group(1), nextLine.group(2))
			apType = nextLine.group(2)
			print "int {0}".format(nextLine.group(1))
			print "  desc {0} - Cisco AP".format(prevLine)
			setOptions(apType)
			prevLine = None

	singleLine = re.match("^([A-Za-z0-9-]+)\s+(\w+\s+[\d/]+).*AIR-CAP(\d+)", line)
	if singleLine:
		#print "Single line: {0} {1}".format(singleLine.group(1), singleLine.group(2))
		apType = singleLine.group(3)
		print "int {0}".format(singleLine.group(2))
		print "  desc {0} - Cisco AP".format(singleLine.group(1))
		setOptions(apType)


    p.sendline ('show int status')
    p.expect('#')

    print ""
    print "! Removing old Meru junk"
    for line in p.before.split('\r\n'):

	findMeru = re.match("^(.*)\s+Meru AP\s+notconnect", line)

	if findMeru:
    		print '! Sanity Check: ', line
		print "default interface", findMeru.group(1)


	

		

logfile.close()

