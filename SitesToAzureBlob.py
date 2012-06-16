from azure.storage.cloudstorageaccount import CloudStorageAccount
from azure.storage.blobservice import BlobService
from bs4 import BeautifulSoup as soup
import os, re

DEVSTORE_CONTAINER_NAME = 'sitestoazure'

class SitesToAzureBlob:
    """
    Class contains functions to upload a static website, which is loacated in a folder, 
    to Windows Azure Blob storage service. 
    """
    def __init__(self, 
                 input_folder, 
                 remove_html_ext = True,
                 over_write = True,
                 account_name = None, 
                 account_key = None, 
                 container_name = DEVSTORE_CONTAINER_NAME):
        '''
        Constructor function. Creates a new container for blobs under the specified account. 
        If the container with the same name already exists, delete it if over_write is true.

        input_folder: The folder contains all the resources of the static website.
        remove_html_ext: Remove the .htm/.html in the url.
        over_write: Delete the existing container.
        account_name: Optional. Your storage account name, DEVSTORE_ACCOUNT_NAME is used if None.
        account_key: Optional. Your storage account key, DEVSTORE_ACCOUNT_KEY is used if None.
        container_name: Optional. Container name, DEVSTORE_CONTAINER_NAME is used if None.
        '''
        self.input_folder = os.path.abspath(input_folder).lower()
        self.remove_html_ext = remove_html_ext
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
 
        if not account_name or not account_key:
            os.environ['EMULATED'] = 'true'
        else:
            os.environ['EMULATED'] = 'false'
 
        self.blob_service = CloudStorageAccount(self.account_name, self.account_key).create_blob_service()
        if over_write:
            self.blob_service.delete_container(container_name)
            
        self.blob_service.create_container(container_name, x_ms_blob_public_access = 'container')
        
    def upload_files_to_blob(self, full_path_blob_name_dict):
        '''
        Uploads the files to the blob.

        full_path_blob_name_dict: A dictionary whose key is the full_path of the file and the value is the blob_name.
        '''

        self.html_blob_name_list = []
        if self.remove_html_ext:
            for blob_name in full_path_blob_name_dict.values():
                file_name, ext = os.path.splitext(blob_name)
                if ext == '.html' or ext == '.htm':
                    self.html_blob_name_list.append(blob_name)

        for full_path, blob_name in full_path_blob_name_dict.iteritems():
            print blob_name + ' is uploading...'

            file_name, ext = os.path.splitext(blob_name)

            file_blob = open(full_path, 'rb').read()
            content_type = self.fetch_content_type(ext)

            if self.remove_html_ext and ext == '.htm' or ext == '.html':
                blob_name = file_name
                file_blob = self.remove_html_extension(file_blob)

            self.blob_service.put_blob(self.container_name, blob_name, file_blob, x_ms_blob_type = 'BlockBlob', x_ms_blob_content_type = content_type)
                
    def list_full_path_with_blob_name(self):
        '''
        Fetches the full_path as key and blob_name as value into a dictionary.
        '''
        dict = {}
        for root, dirs, files in os.walk(self.input_folder):
            for fi in files:
                full_path = os.path.abspath(os.path.join(root, fi)).lower()
                blob_name = self.list_blob_name(full_path)
                dict[full_path] = blob_name.replace('\\', '/') # To replace the Windows backslash \ in the blob_name with /.
        return dict

    def url_rep(self, matchobj):
        '''
        This is called for every non-overlapping occurrence of pattern: href=[\'"]?([^\'" >]+).
        If the matching link url is in html_blob_name_list, remove its extension name, e.g. '.html'.
        '''
        if matchobj.group(1) in self.html_blob_name_list:
            return r'href="' + os.path.splitext(matchobj.group(1))[0] + '"'
        else:
            return matchobj.group(0)

    def remove_html_extension(self, file_content):
        '''
        Removes the .html/.htm extension of the linked html files in the file_content.

        file_content: the content of the html file
        '''
        file_content = re.sub(r'href=[\'"]?([^\'" >]+)', self.url_rep, file_content)

        '''
        Problem with using BeautifulSoup. It cannot preserve the '<', '>' in the <script type="text/template"...>
        '''
        #html = soup(file_content)
        #for tag in html.findAll('a', {'href': True}):
        #    href = tag['href']
        #    if href in html_blob_name_list:
        #        tag['href'] = os.path.splitext(href)[0]
        #return str(html)
        return file_content


    def list_blob_name(self, full_path):
        '''
        Gets the file path names in the input_folder for blob storage.
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
        Fetches the content type from the extension name.
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
    stb = SitesToAzureBlob('../yuqingzhang.com/src/main')
    names_dict = stb.list_full_path_with_blob_name()
    stb.upload_files_to_blob(names_dict)
    

if __name__ == "__main__":
    main()
