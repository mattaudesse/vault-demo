# Vault demo

Please ensure HashiCorp `vault` exists somewhere in your `$PATH` or
fetch the correct platform binary corresponding to v1.11.2 from
[the official downloads page](https://www.vaultproject.io/downloads), verify its
[checksum](https://releases.hashicorp.com/vault/1.11.2/vault_1.11.2_SHA256SUMS),
and unzip it to the root of this repo. Its execute bit must be enabled for the
demo to work (`chmod +x ./vault`).

Once that's sorted, use GNU `make` to trigger the following targets:
```sh
# (You may need to replace `make` with `gmake` depending upon your system)
$ make clean vault # In one terminal
$ make config      # In another
$ make a b         # In a third (or run `a` and `b` separately)
```

The Makefile will automatically stage an isolated Python `venv` and install the
necessary dependencies there.

Running `make a b` should result in the following output:
```sh
Client a triggered 200 when speaking to API a, as expected.
Client a triggered 403 when speaking to API b, as expected.
Client b triggered 403 when speaking to API a, as expected.
Client b triggered 200 when speaking to API b, as expected.
```
