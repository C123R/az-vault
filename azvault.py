#!/usr/bin/env python
import os
import sys
import shlex
import socket
import colorama
import click
from halo import Halo
from subprocess import Popen, PIPE, check_output
from auth import Authentication
from keyvault.command import getList, _isExist, getSecrets, backup_secret, getSecretsList
from common.auth import auth_callback, setCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials


AZVAULT_HOME = os.path.join(os.path.expanduser('~'), '.azvault')
def print_list(ctx, param, value):
    
    output = True
    if not value or ctx.resilient_parsing:
        return
    print(colorama.Fore.GREEN + 'List of Azure Key Vault in your default subscription:\n')
    getList(output)


    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Azure Vault CLI Version 0.1')
    ctx.exit()


@click.group()
@click.help_option('-h','--help', help="Show the usage of azvault.")
@click.option('-v','--version',help="Show the version of azvault", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('-l','--list',is_flag=True,help="List Azure keyVault in current subscription.",callback=print_list,expose_value=False, is_eager=False)
def cli():

    '''
    \b
                                   _ _
     __ _ ____   __   ____ _ _   _| | |_
    / _` |_  /___\ \ / / _` | | | | | __|
    | (_| |/ /_____\ V / (_| | |_| | | |_
    \__,_/___|     \_/ \__,_|\__,_|_|\__|


    \b

    Manage Azure key vaults.

    '''
    
     
@cli.command()
@click.help_option('-h','--help', help="Get the list secrets in specified key vault.")
@click.option('-n','--name',required=True,help="Name of the Azure key vault")
@click.option('-f','--filter',required=False,help="Match string for secrets")
def get(name,filter):

    '''
    To get the secrets from keyvault
    '''

    if filter:
        filter = '*{}*'.format(filter)

        spinner = Halo(text=colorama.Fore.GREEN + 'Getting list of Secrets which matches the pattern {} ..'.format(filter), spinner='dots',color='yellow')
    else:
        spinner = Halo(text=colorama.Fore.GREEN + 'Getting complete list of Secrets for {} ..'.format(name), spinner='dots',color='yellow')
    spinner.start()

    if _isExist(name):
        getSecrets(spinner,name,filter)
    else:
       spinner.fail(colorama.Fore.RED + '{} not a valid Azure Key Vault'.format(name))


@cli.command()
@click.help_option('-h','--help', help="Show the usage of backup command.")
@click.option('-n','--name',required=True,help="Name of the Azure key vault")
def backup(name):

    '''
    To backup azure keyvault
    '''
    spinner = Halo(text=colorama.Fore.GREEN + 'Backing up secrets for {} ..'.format(name), spinner='dots',color='yellow')
    spinner.start()
    if _isExist(name):
        for secret in getSecretsList(name):
            backup_secret(spinner,name,secret)
            
        spinner.succeed(colorama.Fore.GREEN + '{} has been successfully backup under {}'.format(name,AZVAULT_HOME))
    

    else:
        
       spinner.fail(colorama.Fore.RED + '{} not a valid Azure Key Vault'.format(name))



@cli.command()
@click.help_option('-h','--help', help="Show the usage of backup command.")
@click.option('-n','--name',required=True,help="Name of the Azure key vault")
def restore(name):
    
    '''
    To restore the Azure key vault from backup
    '''



@cli.command()
@click.help_option('-h','--help', help="Show the usage of backup command.")
def diff():

    '''
    To check the difference between 2 key vaults
    '''


if __name__ == '__main__':
    
    cli()