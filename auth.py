# Primeras pruebas para generar el XML de autentificacion para la descarga masiva de SAT
import hashlib
import base64

# enlace: https://developers.sw.com.mx/knowledge-base/consumo-webservice-descarga-masiva-sat/

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class peticionAutentificacion:
    fecha = {"inicio": "", "final": ""}
    FIELbytes = ""
    UUIDV4 = ""
    digestValue = ""
    signatureValue = ""

    llavePrivada = ""
    certificado = ""
    contraLlavePrivada = ""

    def __init__(self, fechaInicio, fechaFinal, FIELbytes, ):
        self.fecha["inicio"] = fechaInicio
        self.fecha["final"] = fechaFinal
        self.llavePrivada = FIELbytes

    def _calculateDigestValue(self):
        preDigestValue = hashlib.sha1()
        
        preDigestValue.update("<u:Timestamp xmlns:u=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" u:Id=\"_0\"><u:Created>%s</u:Created><u:Expires>%s</u:Expires></u:Timestamp>" %(self.fecha["inicio"], self.fecha["final"])
        
        return base64.b64encode(preDigestValue.digest())

    def _calculateSIgnatureValue(self):
        preSignatureValue = hashlib.sha1()
        signer = PKCS1_v1_5.new(llavePrivada)

        preSignatureValue.update("<SignedInfo xmlns=\"http://www.w3.org/2000/09/xmldsig#\"><CanonicalizationMethod Algorithm=\"http://www.w3.org/2001/10/xml-exc-c14n#\"></CanonicalizationMethod><SignatureMethod Algorithm=\"http://www.w3.org/2000/09/xmldsig#rsa-sha1\"></SignatureMethod><Reference URI=\"#_0\"><Transforms><Transform Algorithm=\"http://www.w3.org/2001/10/xml-exc-c14n#\"></Transform></Transforms><DigestMethod Algorithm=\"http://www.w3.org/2000/09/xmldsig#sha1\"></DigestMethod><DigestValue>%s</DigestValue></Reference></SignedInfo>" %(self.digestValue))
        
        return signer.sign(preSignatureValue.digest())

    def _create(self):
        body = """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
	<s:Header>
		<o:Security s:mustUnderstand="1" xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
			<u:Timestamp u:Id="_0">
				<u:Created>%s</u:Created>
				<u:Expires>%s</u:Expires>
			</u:Timestamp>
			<o:BinarySecurityToken EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" u:Id="uuid-%s-1">%s</o:BinarySecurityToken>
			<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
				<SignedInfo>
					<CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
					<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
					<Reference URI="#_0">
						<Transforms>
							<Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
						</Transforms>
						<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
						<DigestValue>%s</DigestValue>
					</Reference>
				</SignedInfo>
				<SignatureValue>%s</SignatureValue>
				<KeyInfo>
					<o:SecurityTokenReference>
						<o:Reference URI="#uuid-%s-1" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"/>
					</o:SecurityTokenReference>
				</KeyInfo>
			</Signature>
		</o:Security>
	</s:Header>
	<s:Body>
		<Autentica xmlns="http://DescargaMasivaTerceros.gob.mx"/>
	</s:Body>
</s:Envelope>
        """ %(self.fecha["inicio"], self.fecha["final"], self.UUIDV4, base64.b64encode(self.llavePrivada), self.digestValue, self.signatureValue, self.UUIDV4)



