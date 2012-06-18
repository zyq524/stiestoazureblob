from SitesToAzureBlob import SitesToAzureBlob

def main():
    stb = SitesToAzureBlob('../yuqingzhang.com/src/main', '../yuqingzhang.com/output')
    stb.upload_files_to_blob()
    

if __name__ == "__main__":
    main()