from azure.storage.storageclient import _StorageClient
from azure.storage.blobservice import BlobService
import os, re

DEVSTORE_CONTAINER_NAME="sitestoazure"

class SitesToAzureBlob:
    """

    """
    def __init__(self, 
                 input_folder, 
                 account_name = None, 
                 account_key = None, 
                 container_name = DEVSTORE_CONTAINER_NAME):

        self.input_folder = os.path.abspath(input_folder).lower()

        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name

        if not account_name or not account_key:
            os.environ['EMULATED'] = 'true'
        else:
            os.environ['EMULATED'] = 'false'

        self.storage_account = _StorageClient()
        self.blobService = BlobService(self.storage_account)

        self.blobService.create_container(container_name)

    def list_filename_in_blob(self):
        '''
        Function to get the file path names in the input_folder for blob storage.
        If we uploaded from a subfolder (such as /search), we must rename blobs to have the 'folder/' prefix in their name. 
        For example, if we uploaded index.html from search subfolder, rename the blob from 'index.html' to 'search/index.html'.
        '''
        names = []
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                fullPath = os.path.join(root, file).lower()
                name = fullPath.replace(self.input_folder, '')
                if re.match('[A-Za-z0-9_-]', name[0]) is None:
                    name=name[1:] 
                names.append(name)

                fileName, fileExtension = os.path.splitext(name)
                print name, self.fetch_content_type(fileExtension)

        return names
    
    def fetch_content_type(self, extensionName):
        '''
        Function gets the content type from the extension name.
        '''
        return {
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.jpg':'image/jpg',
            '.jpeg':'image/jpeg',             
            '.mp3':'audio/mp3',            
            '.jar':'application/java-archive',                
            '.zip': 'application/zip',              
            '.htm': 'text/htm',                 
            '.html': 'text/html',                 
            '.js': 'application/javascript',             
            '.txt': 'text/plain',         
            '.css': 'text/css',
            '.xml':'text/xml',
            '.pdf':'application/pdf',
            '.json':'application/json'
            }.get(extensionName, None)    # None is default if extensionName not found       


def main():
    stb=SitesToAzureBlob('../yuqingzhang.com/src/main')
    s=stb.fetch_content_type('.doc')
    names = stb.list_filename_in_blob()
    


if __name__ == "__main__":
    main()
