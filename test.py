from SitesToAzureBlob import SitesToAzureBlob

def main():
    stb = SitesToAzureBlob('../yuqingzhang.com/src/main', '../yuqingzhang.com/output')
    names_dict = stb.list_full_path_with_blob_name()
    stb.upload_files_to_blob(names_dict)
    

if __name__ == "__main__":
    main()