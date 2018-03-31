import requests
from requests import auth
import json
import  docdb

AzureEnvName = 'dev'
class m2cManager(object):

    def __init__(self, authSettings):
        self.authSettings = authSettings

    def getToken(self):
        if self.authSettings:
            client_auth = auth.HTTPBasicAuth(self.authSettings['clientID'] , self.authSettings['clientSecret'])
            post_data = { "grant_type": "client_credentials", "Content-Type": "application/x-www-form-urlencoded" }
            response = requests.post(self.authSettings['accessTokenURL'], auth=client_auth, data=post_data)
            return response.json()['access_token']
        else:
            raise ValueError("Authonetication setting are not defined")

    def getAllB2CUsers(self,graphURL):
        token = self.getToken()
        headers = { "Authorization": "Bearer " + token }
        return requests.get(graphURL, headers= headers).json()

    def getB2CUserByObjectID(self,ObjectID):
        userDetails={}
        token = self.getToken()
        graphURL = self.authSettings['graphBaseURL'] + self.authSettings['b2cTenant'] + '/users/' + ObjectID + '?api-version=1.6' 
        headers = { "Authorization": "Bearer " + token }
        jsondata = requests.get(graphURL, headers= headers).json()
        userDetails['firstName'] = jsondata["surname"]
        userDetails['lastName'] = jsondata["givenName"]
        userDetails['address'] = jsondata["streetAddress"]
        userDetails['emailAddress'] = jsondata["signInNames"][0]["value"]
        return userDetails

    def getb2CUserByFilters(self,filtername):
        userDetails={}
        token = self.getToken()
        graphURL = self.authSettings['graphBaseURL'] + self.authSettings['b2cTenant'] + '/users/' + '?api-version=1.6' + '&$filter=' + filtername
        headers = { "Authorization": "Bearer " + token }
        jsondata = requests.get(graphURL, headers= headers).json()["value"][0]
        userDetails['firstName'] = jsondata["surname"]
        userDetails['lastName'] = jsondata["givenName"]
        userDetails['address'] = jsondata["streetAddress"]
        userDetails['emailAddress'] = jsondata["signInNames"][0]["value"]
        return userDetails

if __name__ == '__main__':
    with open('azureEnv.json', 'r') as f:
        env = json.load(f)
    authSettings = dict(env[AzureEnvName]['graphAPI'])
    dbSettings = dict(env[AzureEnvName]['documentDB'])
    dbclient = docdb.docDB(dbSettings['host'], dbSettings['masterKey'])
    databaseLink = 'dbs/' + dbclient.getAllDatabases()
    collectionLink = databaseLink + '/colls/' + dbclient.getAllCollections(databaseLink)
    #ObjectID = dbclient.getObjectIDbyCommercialRef(collectionLink,'testuser')
    #ObjectID = dbclient.getObjectIDbyMACaddress(collectionLink,'CC-5F-7F-67-DD-37')
    #print(ObjectID)
    b2c = m2cManager(authSettings)
    #allUserURL = 'https://graph.windows.net/debugenvb2c.onmicrosoft.com/users/c965k82d-a595-4913-a0a3-df3hj52ok252e6a?api-version=1.6'
    ObjectID = 'e8e2dd76-c664-4392-82a7-df0c6605f1f4'
    filtername = "givenName eq 'Alkjh' and surname eq 'Hmri'"
    #print(json.dumps(b2c.getB2CUserByObjectID(ObjectID), indent=4))
    print(json.dumps(b2c.getb2CUserByFilters(filtername), indent=4))
    


