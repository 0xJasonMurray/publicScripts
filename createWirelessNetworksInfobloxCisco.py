#!/usr/bin/python

"""
Overview
============
This script is used to create Infoblox networks, DHCP pools, DHCP shares, and
DNS entires for the WUSTL wireless networks.

Wireless networks are allocated in blocks of /19's which are broken
up into /24's.  Each /24 is assigned one PAT overload address.


Usage
===========
Edit this script and change the following variables:
    registrationStart
    productionStart
    vlanStart

Then run it.   It will output cut-and-paste configuration that can be 
imported via the ./ibcli Infoblox command line:

    ibcli -u userName -p myPassword -s gm.example.com wu20expansion.cf
"""


## Example configuration this script needs to create:
##
# Registration Network
#configure network add 172.25.0.0/24 addreverse member 128.252.0.1 member 128.252.0.17 option domain-name-servers="128.252.0.65" option routers="172.25.0.254" option lease-time="30" comment "ibcli created Registration Nework"
#configure zone nts.wustl.edu add host lsb-core-vl666-portal 172.25.0.252
#configure zone nts.wustl.edu add host koenig-core-vl666-portal 172.25.0.253
#configure zone nts.wustl.edu add host hsrp-vl666-portal 172.25.0.254
#configure network add range 172.25.0.1 172.25.0.200 failover DHCP-FailOver macfilter CaptivePortal=deny

# Production Network
#configure network add 172.25.1.0/24 addreverse member 128.252.0.1 member 128.252.0.17 option routers="172.25.1.254" comment "ibcli created Production Nework"
#configure zone nts.wustl.edu add host lsb-core-vl666 172.25.1.252
#configure zone nts.wustl.edu add host koenig-core-vl666 172.25.1.253
#configure zone nts.wustl.edu add host hsrp-vl666 172.25.1.254
#configure network add range 172.25.1.1 172.25.1.200 failover DHCP-FailOver macfilter CaptivePortal=allow

# Shared Network
#conf network add shared vl666-captive-portal comment "Meru Wireless Portal - ResNet" child_network 172.25.0.0/24 child_network 172.25.1.0/24



# guest, portal, encrypted
#networkType='encrypted'
networkType='portal'

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
        print "# Processing instance: " + str(count)


    if createRegNetwork:
        print 'configure network add %s.%d.0/24 addreverse member 128.252.0.1 member 128.252.0.17 option domain-name-servers="128.252.0.65" option routers="%s.%d.254" option lease-time="30" comment "Cisco Wireless Portal %s - vl%d"' % (registrationPrefix, registrationStart, registrationPrefix, registrationStart, ssid, vlanStart)

        print 'configure zone nts.wustl.edu add host vl%d-sgl-svc-portal %s.%d.252' % (vlanStart, registrationPrefix, registrationStart)
        print 'configure zone nts.wustl.edu add host vl%d-eps-svc-portal %s.%d.253' % (vlanStart, registrationPrefix, registrationStart)
        print 'configure zone nts.wustl.edu add host vl%d-hsrp-portal %s.%d.254' % (vlanStart, registrationPrefix, registrationStart)

        print 'configure network add range %s.%d.1 %s.%d.240 failover DHCP-FailOver macfilter CaptivePortal=deny' % (registrationPrefix, registrationStart, registrationPrefix, registrationStart)



    print 'configure network add %s.%d.0/24 addreverse member 128.252.0.1 member 128.252.0.17 option routers="%s.%d.254" comment "Cisco Wireless %s - vl%d"' % (productionPrefix, productionStart, productionPrefix, productionStart, ssid, vlanStart)
    print 'configure zone nts.wustl.edu add host vl%d-sgl-svc %s.%d.252' % (vlanStart, productionPrefix, productionStart)
    print 'configure zone nts.wustl.edu add host vl%d-eps-svc %s.%d.253' % (vlanStart, productionPrefix, productionStart)
    print 'configure zone nts.wustl.edu add host vl%d-hsrp %s.%d.254' % (vlanStart, productionPrefix, productionStart)

    if createRegNetwork:
        print 'configure network add range %s.%d.1 %s.%d.240 failover DHCP-FailOver macfilter CaptivePortal=allow' % (productionPrefix, productionStart, productionPrefix, productionStart)
    else:
        print 'configure network add range %s.%d.1 %s.%d.240 failover DHCP-FailOver' % (productionPrefix, productionStart, productionPrefix, productionStart)

    if createRegNetwork:
        print 'conf network add shared vl%d-captive-portal comment "Cisco Wireless Portal %s" child_network %s.%d.0/24 child_network %s.%d.0/24' % (vlanStart, ssid, productionPrefix, productionStart, registrationPrefix, registrationStart)


    # Counter ++'s
    registrationStart += 1
    productionStart += 1
    vlanStart += 1
    count += 1
