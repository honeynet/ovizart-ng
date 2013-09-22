__author__ = 'eskil@yelp.com'
"""
Adopted from: https://gist.github.com/eskil/2338529

Tools for creating a CA cert and signed server certs.
Divined from http://svn.osafoundation.org/m2crypto/trunk/tests/test_x509.py

The mk_temporary_xxx calls return a NamedTemporaryFile with certs.

Usage ;

   # Create a temporary CA cert and it's private key
   cacert, cakey = mk_temporary_cacert()
   # Create a temporary server cert+key, signed by the CA
   server_cert = mk_temporary_cert(cacert.name, cakey.name, '*.server.co.uk')

"""

import time
from M2Crypto import X509, EVP, RSA, ASN1
import datetime


__all__ = ['createCert']


def mk_cert_valid(cert, days=365):
    """
    Make a cert valid from now and til 'days' from now.
    Args:
       cert -- cert to make valid
       days -- number of days cert is valid for from now.
    """
    t = long(time.time())
    now = ASN1.ASN1_UTCTIME()
    now.set_time(t)
    expire = ASN1.ASN1_UTCTIME()
    expire.set_time(t + days * 24 * 60 * 60)
    cert.set_not_before(now)
    cert.set_not_after(expire)


def mk_request(bits, cn='localhost'):
    """
    Create a X509 request with the given number of bits in they key.
    Args:
      bits -- number of RSA key bits
      cn -- common name in the request
    Returns a X509 request and the private key (EVP)
    """
    pk = EVP.PKey()
    x = X509.Request()
    rsa = RSA.gen_key(bits, 65537, lambda: None)
    pk.assign_rsa(rsa)
    x.set_pubkey(pk)
    name = x.get_subject()
    name.C = "US"
    name.CN = cn
    name.ST = 'CA'
    name.O = 'yelp'
    name.OU = 'testing'
    x.sign(pk, 'sha1')
    return x, pk


def mk_cert():
    """
    Make a certificate.
    Returns a new cert.
    """
    cert = X509.X509()
    cert.set_serial_number(2)
    cert.set_version(2)
    mk_cert_valid(cert)
    cert.add_ext(X509.new_extension('nsComment', 'SSL sever'))
    return cert


def mk_selfsigned_cert():
    """
    Create a CA cert + server cert + server private key.
    """
    # unused, left for history.
    cert_req, pk2 = mk_request(1024, cn=datetime.datetime.now().strftime('ovizart_%Y%m%d_%H%M%S_%f'))
    cert = mk_cert()
    cert.set_subject(cert_req.get_subject())
    cert.set_pubkey(cert_req.get_pubkey())
    cert.sign(pk2, 'sha1')
    return cert, pk2

def createCert():
    import os
    from ovizconf import PROJECT_ROOT

    certFileName = os.path.join(PROJECT_ROOT, 'self-signed-cert.pem')

    # Check file, create if not exists.
    if not os.path.exists(certFileName):
        cert, pk = mk_selfsigned_cert()
        with open(certFileName, 'w') as f:
            f.write(cert.as_pem())
            f.write(pk.as_pem(None))

    # Sanity checks...
    cc = X509.load_cert(certFileName)
    if cc.verify(cc.get_pubkey()) == 1:
        return certFileName
    else:
        return None

# protips
# openssl verify -CAfile cacert.crt cacert.crt cert.crt
# openssl x509 -in cert.crt -noout -text
# openssl x509 -in cacert.crt -noout -text

