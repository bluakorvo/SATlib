import base64
import csv
import zipfile
from io import TextIOWrapper, BytesIO

binFile = ''


def modulo(CSVZipbin):
    datos = []
    csvramzip = BytesIO(CSVZipbin)
    csvziped = zipfile.ZipFile(csvramzip)
    
    files = csvziped.namelist()

    for csv_file in files:
        lab = []

        csv_bin_file = csvziped.open(csv_file, 'r')
        datosAlmacenar = csv.DictReader(TextIOWrapper(csv_bin_file, 'utf-8'), delimiter = '~')
        
    return datosAlmacenar



if __name__ == "__main__":
    var = modulo(base64.b64decode(binFile))

    for element in var:
        print(str(type([''])))
        break

