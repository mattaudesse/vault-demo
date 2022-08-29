import base64
import jwt
import struct
import sys

from cryptography.hazmat.backends                  import default_backend
from cryptography.hazmat.primitives                import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

from flask import Flask, request


# Reconstitute Base64 -> PEM-encoding so PyJWT can understand pubkey
# https://github.com/jpf/okta-jwks-to-pem/blob/1d4b96/jwks_to_pem.py#L22-L47
def pem_of(p):
    def f(d):
        x = base64.urlsafe_b64decode(bytes(d.encode('ascii')) + b'==')
        g = lambda a: int(''.join(['%02x' % b for b in a]), 16)
        return g(struct.unpack('%sB' % len(x), x))

    return RSAPublicNumbers(f(p['e']), f(p['n'])) \
        .public_key(backend=default_backend()) \
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)


def api(n, client_id, port, pubkeys):
    app = Flask('%s/%s:%s' % (__name__, n, str(port)))

    @app.route('/resource')
    def resource():
        h = request.headers['Authorization'][7:]

        def f(k):
            try:
                j = jwt.decode(h, k, audience=client_id, algorithms=['RS256'])
                if 'http://127.0.0.1:%s/resource' % port in j['can_fetch']:
                    return j
                else:
                    return None
            except Exception as e:
                return None

        if all(f(pem_of(k)) == None for k in pubkeys):
            return 'Forbidden', 403
        else:
            return 'OK', 200

    app.run(port=port)
