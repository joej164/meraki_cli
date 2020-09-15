#! /usr/bin/env python

import click
import json

from meraki_api import meraki_api

api = meraki_api()


@click.group()
def meraki_cli():
    pass


@meraki_cli.group()
def network():
    pass


@meraki_cli.group()
def appliance():
    pass


@network.command('add')
@click.argument('network_name', required=True)
@click.option('--tags', help='comma seperated list of tags to apply')
@click.option('--tz', default='America/Los_angeles', help='Timezone to be applied to the network')
def network_add(network_name, tags, tz):
    """Enter the name of the network to add

    NETWORK_NAME is the name you want to exist in your network

    For names with spaces wrap with a pair of quotes 
    """
    tags_list = tags.split(',') if tags else []
    click.echo(f'Creating Network with the following paramters:')
    click.echo(f'{network_name=}')
    click.echo(f'{tags_list=}')
    click.echo(f'{tz=}')
    new_network_id = api.create_meraki_network(network_name, tags_list, tz)
    click.echo(new_network_id)


@network.command('delete')
@click.option('--yes', is_flag=True, help='Enter this to confirm without prompting')
@click.option('--is_id', is_flag=True, help='If the passed in value is a network id instead of a name, use this parameter')
@click.argument('network_name', required=True)
def network_delete(is_id, network_name, yes):
    '''Enter the Network Name or Network ID of a network to delete.

    If passing in a Network ID, set the `is_id` flag'''
    click.echo(f'{is_id=}')
    click.echo(f'{network_name=}')
    click.echo('delete a network')

    to_return = {
        'network_existed': False,
        'network_deleted': False
    }

    if is_id:
        network_info = api.get_meraki_network_details(network_name)
    else:
        network_id_info = api.find_meraki_network_id(network_name)
        if network_id_info:
            network_info = api.get_meraki_network_details(
                network_id_info['id'])
        else:
            network_info = None

    if network_info:
        to_return['network_existed'] = True
        if yes or click.confirm('Are you sure you want to delete this network?'):
            api.delete_meraki_network(network_info['id'])
            to_return['network_deleted'] = True

    click.echo(json.dumps(to_return))


@network.command('site_to_site_vpn')
@click.option('--is_id', is_flag=True, help='If the passed in value is a network id instead of a name, use this parameter')
@click.option('--mode', type=click.Choice(['none', 'spoke', 'hub']), default='hub')
@click.argument('network_name', required=True)
def network_site_to_site_vpn(is_id, network_name, mode):
    '''Enter the Network Name or Network ID of a network to set the
    site to site vpn setting

    If passing in a Network ID, set the `is_id` flag'''
    to_return = {
        'network_existed': False,
        'network_updated': False
    }

    if is_id:
        network_info = api.get_meraki_network_details(network_name)
    else:
        network_id_info = api.find_meraki_network_id(network_name)
        if network_id_info:
            network_info = api.get_meraki_network_details(
                network_id_info['id'])
        else:
            network_info = None

    if network_info:
        to_return['network_existed'] = True
        results = api.set_meraki_network_appliance_site_to_site_vpn_mode(
            network_info['id'], mode)
        click.echo(results)
        to_return['network_updated'] = True

    click.echo(json.dumps(to_return))


@appliance.command('add')
def appliance_add():
    click.echo('add an appliance ')
    click.echo('hello')


@appliance.command('delete')
def appliance_delete():
    click.echo('delete an appliance')


meraki_cli.add_command(network)
meraki_cli.add_command(appliance)
if __name__ == '__main__':
    meraki_cli()
