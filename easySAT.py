# -*- coding: utf-8 -*-

from datetime import datetime

import cfdiclient


class Sat_pet:
    """An easy way to manage and download Metadata and xml reports for SAT"""
    RFC = False

    fiel = False
    passFiel = False

    token = False
    id_download_solicitude = False

    dates = False

    packages_to_download = False

    def __init__(self, RFC, passFiel, fiel_cer, fiel_key, backup=False):
        cer_der = open(fiel_cer, 'rb').read()
        key_der = open(fiel_key, 'rb').read()

        self.passFiel = passFiel
        self.RFC = RFC
        self.fiel = cfdiclient.Fiel(cer_der, key_der, passFiel)

        if backup:
            self.RFC = backup['RFC']
            self.token = backup['token']

    def make_auth(self):
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

    def make_download_petition(self, RFC_emissor=False, RFC_receiver=None, only_metadata=True):
        if not self.dates:
            return "ERROR: to continue the app need the dates to look on index"

        type_of_download = 'Metadata'

        if not RFC_emissor and RFC_receiver is None:
            RFC_emissor = self.RFC

        if not only_metadata:
            type_of_download = 'CFDI'

        download = cfdiclient.solicitadescarga.SolicitaDescarga(self.fiel)

        result = download.solicitar_descarga(self.token, self.RFC, self.dates['start'], self.dates['end'],
                                             rfc_emisor=RFC_emissor, rfc_receptor=RFC_receiver,
                                             tipo_solicitud=type_of_download)

        self.id_download_solicitude = result['id_solicitud']

        print(result)

    def verify_download_petition(self):
        verify_download_solicitude = cfdiclient.verificasolicituddescarga.VerificaSolicitudDescarga(self.fiel)

        data = verify_download_solicitude.verificar_descarga(self.token, self.RFC, self.id_download_solicitude)

        self.packages_to_download = data['paquetes']

        print(data)

    def download_packages(self):
        if len(self.packages_to_download) == 0:
            return "ERROR: you maybe miss a step to download (all) the zip package(s)"

        download = cfdiclient.descargamasiva.DescargaMasiva(self.fiel)

        data = []

        for pack in self.packages_to_download:
            data.append(download.descargar_paquete(self.token, self.RFC, pack))

        return data

    def save_as_dic(self):
        return {'token': self.token,
                'RFC': self.RFC,
                'dates': self.dates,
                'id_download_solicitude': self.id_download_solicitude,
                'packages_to_download': self.packages_to_download}

    def __str__(self):
        return "RFC: %s\nToken: %s\nFechas: %s\nIDDescarga: %s\nCantidad de paquetes: %s" % (
        self.RFC, self.token, self.dates, self.id_download_solicitude, self.packages_to_download)