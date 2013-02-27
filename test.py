from SitesToAzureBlob import SitesToAzureBlob

def main():
    stb = SitesToAzureBlob('../yuqingzhang.com/src/main', '../yuqingzhang.com/output', overwrite_output = False, account_name = 'zhangyuqinglabs', account_key = 'zbC/2jangIEmAeKVE0c7KybQl8TwgEkGIK5tpnTJku0CUudDZR/mytqtJw2I/OiwKFZVMiVVWYKVjxMwpUQQbQ==',
                         container_name = 'site')
    stb.upload_files_to_blob()
    

if __name__ == "__main__":
    main()