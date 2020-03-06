from easySAT import Sat_pet as sat

user = sat('MTN040706LVA', 'Abcd1234', r'mtn040706lva.cer', r'Claveprivada_FIEL_MTN040706LVA_20170225_123500.key')

if __name__ == "__main__":
    user.create_dates('2019', '11', '9', '2019', '12', '9')
    user.make_download_petition()
    user.download_packages(save_as_files = True)
    
    var = user.return_requested_data()
    
    for element in var:
        print(element)



