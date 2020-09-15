# meraki_cli
Meraki CLI Tool

# Overview
This is a command line tool to be used in the automating of the Meraki VMX.

# Installation

# Configuration


# Examples

## Add a Network to an ORG
`./meraki_cli.py network add 'new network'`     # Add a network

`./meraki_cli.py network add 'new network' --tags tag1,tag2`     # Add a network with tags

`./meraki_cli.py network add 'new network' --tz America/Los_angeles`     # Add a network a timezone set

## Update a Network VPN Settings
`./meraki_cli.py network site_to_site_vpn 'new network'`  # Set the site to site vpn to hub mode

`./meraki_cli.py network site_to_site_vpn 'new network' --mode none`  # Set the site to site vpn to none

`./meraki_cli.py network site_to_site_vpn 'N_61530429908953XXXX' --is_id --mode none`  # Set the site to site vpn to none using a network ID instead of a name

## Delete a Network
`./meraki_cli.py network delete 'new network'`  # Delete a network 

`./meraki_cli.py network delete 'N_61530429908953XXXX' --is_id --yes`  # Set the site to site vpn to none using a network ID instead of a name and no confirmation is required
