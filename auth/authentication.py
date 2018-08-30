from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.mgmt.keyvault import KeyVaultManagementClient
try:
    from azure.common.credentials import ServicePrincipalCredentials
except ImportError:
    raise ImportError("You need to install azure-common for the authorization")

class Authentication:

    """Configuration for KeyVaultClient
    Credentials object for Service Principle Authentication.
    Authenticates via a Client ID and Secret.
    :param client_id: Azure Client ID
    :param secret_id: Azure Secret ID
    :param tenant_id: Azure Tenant ID
    :param resource: Azure Resource

    """

    def __init__(
        self,client_id,secret_id,tenant_id,resource,subscription_id):

        if client_id is None:
            raise ValueError("Parameter 'client_id' must not be None.")
        if secret_id is None:
            raise ValueError("Parameter 'secret_id' must not be None.")
        if tenant_id is None:
            raise ValueError("Parameter 'tenant_id' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")
        if not resource:
            resource = 'https://management.core.windows.net'

        self.client_id = client_id
        self.secret_id = secret_id
        self.tenant_id = tenant_id
        self.resource  = resource
        self.subscription_id = subscription_id


    def get_credentials(self):

        """Returns Credentials object for Service Principle Authentication.
        Authenticates via a Client ID and Secret.
        """
        credentials = ServicePrincipalCredentials(

            client_id= self.client_id,
            secret= self.secret_id,
            tenant= self.tenant_id,
            resource= self.resource
        )

        return credentials


    def get_accessToken(server, resource, scope):

        """Returns Access Token object for Service Principle Authentication.
        Authenticates via a Client ID and Secret.
        """

        credentials = ServicePrincipalCredentials(

            client_id=self.client_id,
            secret=self.secret_id,
            tenant=self.tenant_id,
            resource="https://vault.azure.net"
        )

        token = credentials.token
        return token['access_token']


    def getClient(self):
        
        
        kvClient = KeyVaultClient
        (
            KeyVaultAuthentication
            (
                self.get_accessToken
            )
        )

        return kvClient


    def getMgmtClient(self):
        
        
        kvMgmtClient = KeyVaultManagementClient
        (
            self.get_credentials,
            self.subscription_id
        )
    
        return kvMgmtClient

    