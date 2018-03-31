import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client
import pydocumentdb.errors as errors
import datetime
import json

#AzureEnvName = 'debug'
class docDB:

    def __init__(self,host,masterKey):

        self.client = document_client.DocumentClient(host, {'masterKey': masterKey})
    
    def getAllDatabases(self):
        databases = list(self.client.ReadDatabases())
        if not databases:
            return
        for database in databases:
             return database['id']

    def getAllCollections(self,databaseLink):
       collections = list(self.client.ReadCollections(databaseLink))
       if not collections:
           return
       for collection in collections:
          return collection['id']

    def getAllDocuments(self,collectionLink):
        documentlist = list(self.client.ReadDocuments(collectionLink, {'maxItemCount':10}))
        
        print('Found {0} documents'.format(documentlist.__len__()))
        
        for doc in documentlist:
            print('Document Id: {0}'.format(doc.get('id')))

    def getDocumentByQuery(self,collectionLink,query):
        try:
           results = list(self.client.QueryDocuments(collectionLink, query))
           return results[0]
        except  errors.HTTPFailure as e:
           raise errors.HTTPFailure(e.status_code)

    def getObjectIDbyCommercialRef(self,collectionLink,CommercialRef):
        queryByCommercialRef = { 
                                 "query": "select * from docs d where d.DeviceProperties.CommercialRef = @CommercialRef ",
                                 "parameters": [  { "name": "@CommercialRef", "value": CommercialRef } ]
                               }
        return self.getDocumentByQuery(collectionLink,queryByCommercialRef)['DeviceUsers'][0]['UserId']

    def getObjectIDbyMACaddress(self,collectionLink,macaddress):
        queryByMACaddress = { 
                                 "query": "select * from docs d where d.DeviceProperties.MACAddress = @macaddress ",
                                 "parameters": [  { "name": "@macaddress", "value": macaddress } ]
                               }
        return self.getDocumentByQuery(collectionLink,queryByMACaddress)['DeviceUsers'][0]['UserId']
'''
if __name__ == '__main__':
    with open('azureEnv.json', 'r') as f:
        env = json.load(f)

    masterKey = env[AzureEnvName]['documentDB']['masterKey']
    host = env[AzureEnvName]['documentDB']['host']
    #DBclient = document_client.DocumentClient(host, masterKey)
    doc = docDB(host,masterKey)

    databaseLink = 'dbs/' + doc.getAllDatabases()
    collectionLink = databaseLink + '/colls/' + doc.getAllCollections(databaseLink)

    queryByMacAddress = { "query": "select * from docs d where d.DeviceProperties.MACAddress = '6E-mo-00-3D-22-1C' " }  
    queryByUserId = { "query": "select * from docs d where d.DeviceUsers[0].UserId = 'c916672d-a595-4913-a0a3-df3c65c52e6a' " }  
    queryByDeviceID = { "query": "select * from docs d where d.DeviceProperties.DeviceID = @deviceID ",
                        "parameters": [  { "name": "@deviceID", "value": "956mklh87d9-875a-4f57-9245-ejh52d478d463" } ] 
                      }  
    print(doc.getObjectIDbyCommercialRef(collectionLink,'HamzaA'))
'''
