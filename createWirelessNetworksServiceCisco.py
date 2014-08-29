#!/usr/bin/python

"""
Overview
============
This script is used to create Cisco layer 3 interfaces for the WUSTL 
wireless networks.

Wireless networks are allocated in blocks of /19's which are broken
up into /24's.  Each /24 is assigned one PAT overload address.


Usage
===========
Edit this script and change the following variables:
    registrationStart
    productionStart
    vlanStart
    routerLocation

Then run it.   It will output cut-and-paste configuration.
"""



## Example output that needs to be created from this sript:
##
#  interface Vlan2161
#  description cisco wireless wustl portal 2.0 vl2161
#  ip vrf forwarding wl-2-0
#  ip address 172.25.125.253 255.255.255.0 secondary
#  ip address 172.27.61.253 255.255.255.0
#  ip helper-address 128.252.0.1
#  ip helper-address 128.252.0.17
#  no ip redirects
#  no ip unreachables
#  no ip proxy-arp
#  ip flow ingress
#  ip flow egress
#  standby 0 ip 172.27.61.254
#  standby 0 priority 105
#  standby 0 preempt
#  standby 0 authentication md5 key-chain nss_hsrp
#  standby 1 ip 172.25.125.254
#  standby 1 priority 105
#  standby 1 preempt
#  standby 1 authentication md5 key-chain nss_hsrp
# end

# interface Vlan2161
#  description cisco wireless wustl portal 2.0 vl2161
#  ip vrf forwarding wl-2-0
#  ip address 172.25.125.252 255.255.255.0 secondary
#  ip address 172.27.61.252 255.255.255.0
#  ip helper-address 128.252.0.1
#  ip helper-address 128.252.0.17
#  no ip redirects
#  no ip unreachables
#  no ip proxy-arp
#  ip flow ingress
#  ip flow egress
#  standby 0 ip 172.27.61.254
#  standby 0 preempt
#  standby 0 authentication md5 key-chain nss_hsrp
#  standby 1 ip 172.25.125.254
#  standby 1 preempt
#  standby 1 authentication md5 key-chain nss_hsrp
# end


# guest, portal, encrypted
#networkType='encrypted'
networkType='portal'

# eps, sgl
routerLocation = 'eps'
#routerLocation = 'sgl'

#productionRun = False
productionRun = True

# Always 32 networks for Cisco (/19 equiv)
totalNetworks=32

# Network prefixes
registrationPrefix='172.25'
productionPrefix='172.27'


if networkType == 'guest':
    # wustl-guest-2.0 ssid
    ssid = 'wustl-guest-2-0'
    registrationStart=96
    productionStart=0
    vlanStart=2100
    createRegNetwork=False


if networkType == 'portal':
    # wustl-2.0 ssid
    ssid = 'wustl-2-0'
    registrationStart=192
    productionStart=96
    vlanStart=2196
    createRegNetwork=True


if networkType == 'encrypted':
    # wustl-2.0 ssid
    ssid = 'wustl-encrypted-2-0'
    registrationStart=0
    productionStart=128
    vlanStart=2228
    createRegNetwork=False



count = 0
while count < 32:
    if productionRun == False:
        print ""
        print "; Processing instance: " + str(count)

    print "interface Vlan%d" % (vlanStart)
    print " description cisco wireless %s 2.0 vl%d" % (ssid, vlanStart)
    print " ip vrf forwarding wl-2-0"
    if routerLocation == 'eps':
        print " ip address %s.%s.253 255.255.255.0" % (productionPrefix, productionStart)
    if routerLocation == 'sgl':
        print " ip address %s.%s.252 255.255.255.0" % (productionPrefix, productionStart)
    if createRegNetwork:
        if routerLocation == 'eps':
            print " ip address %s.%s.253 255.255.255.0 secondary" % (registrationPrefix, registrationStart)
        if routerLocation == 'sgl':
            print " ip address %s.%s.252 255.255.255.0 secondary" % (registrationPrefix, registrationStart)
    print " ip helper-address 128.252.0.1"
    print " ip helper-address 128.252.0.17"
    print " no ip redirects"
    print " no ip unreachables"
    print " no ip proxy-arp"
    print " ip flow ingress"
    print " ip flow egress"
    print " standby 0 ip %s.%s.254" % (productionPrefix, productionStart)
    if routerLocation == 'eps':
        print " standby 0 priority 105"
    print " standby 0 preempt"
    print " standby 0 authentication md5 key-chain nss_hsrp"
    if createRegNetwork:
        print " standby 1 ip %s.%s.254" % (registrationPrefix, registrationStart)
        if routerLocation == 'eps':
            print " standby 1 priority 105"
        print " standby 1 preempt"
        print " standby 1 authentication md5 key-chain nss_hsrp"
        print " no shut"


    # Counter ++'s
    registrationStart += 1
    productionStart += 1
    vlanStart += 1
    count += 1

