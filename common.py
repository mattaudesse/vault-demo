import hvac
import sys


ports = dict(a=8210, b=8220)


def vault():
    with open('./vout', 'r') as v:
        l = v.readlines()

    t = next((a[12:-1] for a in l if a.startswith('Root Token')), None)
    u = next((a[25:-2] for a in l if 'export VAULT_ADDR' in a),   None)

    def bail_without(b, n):
        if b is None or len(b) < 1:
            print("Couldn't parse %s!" % n)
            sys.exit(1)

    bail_without(t, 'Root Token')
    bail_without(u, 'VAULT_ADDR')

    c = hvac.Client(url=u, token=t)
    x = False

    try:
        x = c.is_authenticated()
    finally:
        if not x:
            print("Couldn't authenticate with vault at %s using token: %s" % (u, t))
            sys.exit(1)

    return c
