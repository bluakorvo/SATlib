# -*- coding: utf-8 -*-

from datetime import datetime

import cfdiclient, base64, hashlib

# Esto es solo para mero debug, eliminar en la linea proinciapal

import time


class Sat_pet:
    """An easy way to manage and download Metadata and xml reports for SAT"""
    RFC = False

    fiel = False
    passFiel = False

    token = False
    id_download_solicitude = False

    dates = False

    packages_to_download = False
    downloaded_packages = False

    def __init__(self, RFC, passFiel, fiel_cer, fiel_key, backup=False):
        cer_der = open(fiel_cer, 'rb').read()
        key_der = open(fiel_key, 'rb').read()

        self.passFiel = passFiel
        self.RFC = RFC
        self.fiel = cfdiclient.Fiel(cer_der, key_der, passFiel)

        self._make_auth()

        if backup:
            self.RFC = backup['RFC']

    def _make_auth(self):
        auth = cfdiclient.autenticacion.Autenticacion(self.fiel)

        self.token = auth.obtener_token()

        if self.token != '':
            return True

        return False

    def create_dates(self, start_year, start_month, start_day, end_year, end_month, end_day):
        try:
            self.dates = {'start': datetime(int(start_year), int(start_month), int(start_day)),
                          'end': datetime(int(end_year), int(end_month), int(end_day))}
        except:
            self.dates = False
            return False

    def make_download_petition(self, RFC_emissor=None, RFC_receiver=None, only_metadata=True):
        if not self.dates:
            return "ERROR: to continue the app need the dates to look on index"

        type_of_download = 'Metadata'

        if RFC_emissor is None and RFC_receiver is None:
            RFC_emissor = self.RFC

        if not only_metadata:
            type_of_download = 'CFDI'

        download = cfdiclient.solicitadescarga.SolicitaDescarga(self.fiel)

        result = download.solicitar_descarga(self.token, self.RFC, self.dates['start'], self.dates['end'],
                                             rfc_emisor=RFC_emissor, rfc_receptor=RFC_receiver,
                                             tipo_solicitud=type_of_download)

        self.id_download_solicitude = result['id_solicitud']

        # print(result)

        if self.id_download_solicitude is None:
            return False
        
        return True;

    def _verify_download_petition(self):
        verify_download_solicitude = cfdiclient.verificasolicituddescarga.VerificaSolicitudDescarga(self.fiel)

        

        data = verify_download_solicitude.verificar_descarga(self.token, self.RFC, self.id_download_solicitude)
        
        self.packages_to_download = data['paquetes']
        # print(data)
        return data

    def download_packages(self, save_as_files = False):
        download_petition = self._verify_download_petition()

        # SEccion de debuggin
        while True:
            if download_petition['estado_solicitud'] != '3':
               download_petition = self._verify_download_petition()
               print("---------esperando respuesta positiva DEBUGGIN----------")
               print(download_petition)
               time.sleep(30)

            else:
                break
        # Fin del Debugging
        # if not self.packages_to_download:
            # download_petition = self._verify_download_petition()

        download = cfdiclient.descargamasiva.DescargaMasiva(self.fiel)

        data = []

        for pack in self.packages_to_download:
            package = download.descargar_paquete(self.token, self.RFC, pack)
            data.append(package['paquete_b64'])

        if save_as_files:
            for archive in data:
                self.save_file(archive, 1)
        
        return data

    def save_file(self, archivo, ID):

        print("EstadoDeCosa:", archivo)
        with open(ID + ".zip", "wb") as file:
            file.write(base64.b64decode(archivo))
            file.close()
        
    def save_as_dict(self):
        return {'RFC': (self.RFC, self.RFC),
                'dates': self.dates,
                'id_download_solicitude': self.id_download_solicitude}

    def __str__(self):
        return "RFC: %s\nToken: %s\nFechas: %s\nIDDescarga: %s\nCantidad de paquetes: %s paquetes: %s" % (
        self.RFC, self.token, self.dates, self.id_download_solicitude, self.packages_to_download, self.downloaded_packages)
