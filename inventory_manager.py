import os
import yaml
import json
import copy
import click

def add_public_inventory(old_inventory, new_inventory):
    public_inventory = old_inventory
    data = new_inventory
    for host in data:
        groups = data[host]['group_names']
        item = {
            "ansible_host": data[host]['ansible_host'],
            "ansible_user": data[host]['ansible_user']
        }
        if data[host].get('ansible_password') is not None:
            item['ansible_password'] = data[host]['ansible_password']
        if data[host].get('ansible_ssh_private_key') is not None:
            item['ansible_ssh_private_key'] = data[host]['ansible_ssh_private_key']
        if data[host].get('internal_ip') is not None:
            item['internal_ip'] = data[host]['internal_ip']
        for group in groups:
            if group not in public_inventory.keys():
                public_inventory[group] = {}
                public_inventory[group]['hosts'] = {}
            copied_item = copy.deepcopy(item)
            public_inventory[group]['hosts'][data[host]['inventory_hostname']] = copied_item
    return public_inventory


def add_private_inventory(old_inventory, new_inventory):
    private_inventory = old_inventory
    data = new_inventory
    for host in data:
        print(host)
        groups = data[host]['group_names']
        item = {
            "ansible_host": data[host]['internal_ip'],
            "ansible_user": data[host]['internal_user'],
            "ansible_ssh_private_key": data[host]['ansible_ssh_private_key'],
            "ansible_ssh_common_args": '-o ProxyCommand="ssh -W %h:%p -o StrictHostKeyChecking=no -q {}@{}"'.format(data[host]['internal_user'], data[host]['bastion_ip'])
        }
        for group in groups:
            if group not in private_inventory.keys():
                private_inventory[group] = {}
                private_inventory[group]['hosts'] = {}
            copied_item = item.copy()
            private_inventory[group]['hosts'][data[host]['inventory_hostname']] = copied_item
    return private_inventory

def remove_inventory(old_inventory, groups, server_name):
    inventory = old_inventory.copy()
    for g in groups:
        del inventory[g]['hosts'][server_name]
        if inventory[g]['hosts'] == {}:
            del inventory[g]
    return inventory


@click.group()
def cli():
    click.echo("Inventory manager")

@cli.command()
@click.option('--datacentre', default=False, type=str)
@click.option('--public', default=False, type=bool)
@click.option('--input', default=False, type=str)
def add(datacentre, public, input):
    click.echo("Add inventory")
    inventory_file_name = "./inventories/{}_{}_inventory.yaml".format(datacentre, 'public' if public is True else 'private')
    if os.path.exists(inventory_file_name):
        with open(inventory_file_name, 'r') as initialfile:
            old_inventory = yaml.safe_load(initialfile)
    else:
        old_inventory = {}
    with open(input, 'r') as infile:
        raw_data = infile.read()
    new_inventory = json.loads(raw_data)
    if public:
        inventory = add_public_inventory(old_inventory, new_inventory)
    else:
        inventory = add_private_inventory(old_inventory, new_inventory)
    with open(inventory_file_name, 'w') as outfile:
        yaml.safe_dump(inventory, outfile, default_flow_style=False, encoding='utf-8', allow_unicode=True)

@cli.command()
@click.option('--datacentre', default=False, type=str)
@click.option('--public', default=False, type=bool)
@click.option('--groups', default=False, type=str)
@click.option('--server', default=False, type=str)
def remove(datacentre, public, groups, server):
    click.echo("Remove inventory")
    inventory_file_name = "./inventories/{}_{}_inventory.yaml".format(datacentre, 'public' if public is True else 'private')
    if os.path.exists(inventory_file_name):
        with open(inventory_file_name, 'r') as initialfile:
            old_inventory = yaml.safe_load(initialfile)
    else:
        old_inventory = {}
    groups = groups.split(",")
    inventory = remove_inventory(old_inventory, groups, server)
    with open(inventory_file_name, 'w') as outfile:
        yaml.safe_dump(inventory, outfile, default_flow_style=False, encoding='utf-8', allow_unicode=True)

if __name__ == '__main__':
    cli()
