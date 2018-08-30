import os
import sys
import shlex
import socket
import colorama
import click
import fnmatch
from halo import Halo
from subprocess import Popen, PIPE, check_output
from auth import Authentication
from common.auth import auth_callback, setCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials
from prettytable import PrettyTable

credentials, subscription_id = setCredentials()
kvclientMgmt = KeyVaultManagementClient(credentials, subscription_id )
kvclient = KeyVaultClient(KeyVaultAuthentication(auth_callback))



AZVAULT_HOME = os.path.join(os.path.expanduser('~'), '.azvault')

def getList(output=False):
    
    keyVaultList = []

    for vault in kvclientMgmt.vaults.list():
        
        keyVaultList.append(vault.name)
        if output:
           
            print("- " + vault.name)
           
    return keyVaultList


def _isExist(keyVault_name):
    
    '''
    
    Check if the provided name is present in current subscription


    Return: True or False 

    '''
    if keyVault_name in getList():
        return True
    else:
        return False     


def getSecretsList(keyVault_name):
    

    secretList = []
    base_url = 'https://{}.vault.azure.net'.format(keyVault_name)

    for secret in kvclient.get_secrets(vault_base_url=base_url):
        secret_name = (secret.id.rsplit('/', 1)[1])
        secretList.append(secret_name)

    return secretList


def backup_secret(spinner,vault_name, secret_name):
    

    base_url = 'https://{}.vault.azure.net'.format(vault_name)
    backup = kvclient.backup_secret(base_url, secret_name).value

    vault_path = os.path.join(AZVAULT_HOME, vault_name)
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)

    secret = os.path.join(vault_path, secret_name)

    with open(secret, 'wb') as out:
        out.write(backup)



def getSecrets(spinner,keyVault_name,filter=None):


    vaultSecrets = {}

    base_url = 'https://{}.vault.azure.net'.format(keyVault_name)

    if filter:
        secrets = fnmatch.filter(getSecretsList(keyVault_name), filter)
    else:
        secrets = getSecretsList(keyVault_name)


    for secret in secrets:

        secret_bundle = kvclient.get_secret(base_url, secret,'')
        vaultSecrets[secret] = secret_bundle.value

    

    spinner.succeed(colorama.Fore.GREEN + 'List of Secrets in --> ({}):'.format(keyVault_name))
    header = ['Secret Name','Secret Value']
   # _print_table(vaultSecrets,header)
    for k, v in vaultSecrets.items():
        
        print('{} : {}'.format(k,v))
  
    return vaultSecrets




        
        

