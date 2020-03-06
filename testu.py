from easySAT import Sat_pet as sat

user = sat('file', '', r'file.cer', r'file.key')

if __name__ == "__main__":
    user.create_dates('2019', '11', '9', '2019', '12', '9')
    user.make_download_petition()
    user.download_packages(save_as_files = True)
    
    var = user.return_requested_data()
    
    for element in var:
        print(element)



