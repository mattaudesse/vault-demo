import json

from threading import Thread

from api    import api
from common import vault, ports


def main():
    c = vault()
    i = c.secrets.identity

    if 'oidc/' not in c.sys.list_auth_methods():
        c.sys.enable_auth_method(method_type='oidc')

    if 'approle/' not in c.sys.list_auth_methods():
        c.sys.enable_auth_method(method_type='approle')

    i.create_named_key(name='key')

    def ident_for(r):
        i.create_or_update_role(
            name=r,
            key='key',
            template=json.dumps(dict(
                can_fetch=['http://127.0.0.1:%s/resource' % ports[r]])))

        return i.read_role(name=r)['data']['client_id']

    a = ident_for('a')
    b = ident_for('b')

    # This is actually an upsert
    i.create_named_key(name='key', allowed_client_ids=[a, b])

    c.sys.create_or_update_policy(
        name='demo',
        policy={'path': {'*': {'capabilities': ['create', 'read', 'list']}}})

    def login_for(r):
        x = c.auth.approle
        n = 'login_%s' % r

        x.create_or_update_approle(role_name=n, token_policies=['demo'])
        x.update_role_id(role_name=n, role_id=n)

        with open('./cred/%s' % r, 'w') as s:
            s.write(x.generate_secret_id(role_name=n)['data']['secret_id'])

    login_for('a')
    login_for('b')

    # N.B. Vault always provides a `default` key pair as well, but we've
    # created a new key of our own above and restricted its access to just our
    # `a` and `b` clients, so consequently p's length will be 2. AFAICT there's
    # no reliable way of retrieving the single pubkey we need based on a name
    # or tag, so instead we'll just attempt verification with both.
    p = c.secrets.identity.read_active_public_keys()['keys']

    Thread(target=api, args=('a', a, ports['a'], p)).start()
    Thread(target=api, args=('b', b, ports['b'], p)).start()


if __name__ == '__main__':
    main()
