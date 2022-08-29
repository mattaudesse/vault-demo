import requests
import sys

from common import vault, ports


def main(role):
    c = vault()

    with open('./cred/%s' % role, 'r') as s:
        c.auth.approle.login(role_id='login_%s' % role, secret_id=s.read())

    l = c.secrets.identity.generate_signed_id_token(name=role)['data']['token']

    def ensure(r, n):
        s = requests.get(
            'http://127.0.0.1:%s/resource' % ports[r],
            headers={'Authorization': 'Bearer %s' % l}).status_code

        if not s == n:
            print("Client %s didn't trigger %s when speaking to API %s! Received %s instead." \
                % (role, n, r, s))
            sys.exit(1)
        else:
            print('Client %s triggered %s when speaking to API %s, as expected.' \
                % (role, n, r))

    ensure('a', 200 if role == 'a' else 403)
    ensure('b', 200 if role == 'b' else 403)


if __name__ == '__main__':
    main(sys.argv[1])
