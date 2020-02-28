
from lxml import etree, objectify
from io import StringIO, BytesIO

import hashlib
import base64

#----------------------------------------------------------------------
    
"""
"""

#----------------------------------------------------------------------
def get_etree(pathFile):
    parser = etree.XMLParser(remove_blank_text=True, ns_clean=True, collect_ids=False)
    return etree.parse(pathFile, parser)

def get_obectify(pathFile):
    return objectify.parse(pathFile)

def imprimirArbol(data):
    for child in data:
        print("+", child.tag)
        for hijo in child:
            print("+----> %s" % (hijo.tag))
            for t in hijo:
                print("|-------+> %s" % (t.tag))
                for u in t:
                    print("        |----> %s: %s" % (u.tag, u.text))

#----------------------------------------------------------------------
if __name__ == "__main__":
    f = r'fileTest.xml'
    xml1 = get_etree(f)
    xml2 = get_obectify(f)

    print(xml1)
    print(xml2)

    print("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>")

    root = xml1.getroot()
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    #imprimirArbol(root)
    
    mod = root.findall(".//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Timestamp")
    """
    print(mod[0].text)
    mod[0].text = "GG IZ"
    print(mod[0].text)
    """
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    txt = etree.tostring(mod[0])
    print("------------")
    etree.cleanup_namespaces(mod[0],)
    print("-------<>-------")
    lrm = etree.XML('<u:Timestamp xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" u:Id="_0"><u:Created>2019-01-09T16:48:50.000Z</u:Created><u:Expires>2019-01-09T16:53:50.000Z</u:Expires></u:Timestamp>')

    for child in lrm:
        print(child.tag)

    print(etree.tostring(lrm, pretty_print=False))
    print("-------<>-------")
    print(str(txt))
    # txt = str(txt, 'utf-8')
    # mod[0].xpath("//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Timestamp[@xmlns:o=\'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/\'")

    preValue = hashlib.sha1()
    preValue.update(etree.tostring(mod[0]))
    print(preValue.digest())
    print(base64.b64encode(preValue.digest()))
    


