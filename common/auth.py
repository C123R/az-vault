import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication

subscription_id=os.environ['ARM_SUBSCRIPTION_ID']

def setCredentials(resource=None):
    

    if resource is None:
        credentials = ServicePrincipalCredentials(
            client_id=os.environ['ARM_CLIENT_ID'],
            secret=os.environ['ARM_CLIENT_SECRET'],
            tenant=os.environ['ARM_TENANT_ID']
        )
        return credentials,subscription_id
    
    else:
            credentials = ServicePrincipalCredentials(
            client_id=os.environ['ARM_CLIENT_ID'],
            secret=os.environ['ARM_CLIENT_SECRET'],
            tenant=os.environ['ARM_TENANT_ID'],
            resource=resource
        )
    return credentials



def auth_callback(server, resource, scope):
    
    token = setCredentials("https://vault.azure.net").token

    return token['token_type'], token['access_token']

