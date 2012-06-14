from azure.storage.storageclient import _StorageClient
from azure.storage.cloudstorageaccount import CloudStorageAccount
from azure.storage.blobservice import BlobService
import os, re

DEVSTORE_CONTAINER_NAME = 'sitestoazure'

class SitesToAzureBlob:
    """

    """
    def __init__(self, 
                 input_folder, 
                 over_write = True,
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
 
#        self.storage_account = _StorageClient(account_name, account_key)
#        self.blob_service = BlobService(self.storage_account)
        self.blob_service = CloudStorageAccount(self.account_name, self.account_key).create_blob_service()
        if over_write:
            self.blob_service.delete_container(container_name)
            
        self.blob_service.create_container(container_name, x_ms_blob_public_access='container')
        
    def upload_files_to_blob(self):
        for root, dirs, files in os.walk(self.input_folder):
            for fi in files:
                full_path = os.path.abspath(os.path.join(root, fi)).lower()
                blob_path = self.list_filename_in_blob(full_path)
                root, ext = os.path.splitext(blob_path)
                if ext == '.htm' or ext == '.html':
                    blob_path = root
                file_blob = open(full_path, 'r').read()
                content_type = self.fetch_content_type(ext)
                self.blob_service.put_blob(self.container_name, blob_path, file_blob, x_ms_blob_type = 'BlockBlob', 
                                           x_ms_blob_content_type = content_type)
                print blob_path + ' uploaded'
                
    def list_filename_in_blob(self, full_path):
        '''
        Function to get the file path names in the input_folder for blob storage.
        If we uploaded from a subfolder (such as /search), we must rename blobs to have the 'folder/' prefix in their name. 
        For example, if we uploaded index.html from search subfolder, rename the blob from 'index.html' to 'search/index.html'.
        '''
        name = full_path
        name = name.replace(self.input_folder, '')
        if re.match('[A-Za-z0-9_-]', name[0]) is None:
            name=name[1:] 
        return name
    
    def fetch_content_type(self, extension_name):
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
            }.get(extension_name, None)    # None is default if extensionName not found       


def main():
    stb=SitesToAzureBlob('../yuqingzhang.com/src/main', account_name='zhangyuqinglabs', account_key='0Pmad0vCkugnhX/USyVvDPXMDH8smY8uJqQBZHs9DHMrmALhpDNE5ey6gjEcbzWef4kCbwAxOlxOS5Kvsp0N/A==')
    stb.upload_files_to_blob()
    


if __name__ == "__main__":
    main()
