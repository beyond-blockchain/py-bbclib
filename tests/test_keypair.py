from authlib.jose import JsonWebKey
import hashlib
import json

import sys
sys.path.append('.')
sys.path.append('..')


import bbclib


class TestKey(object):

    def test_01_key_compare(self):
        print("\n-----", sys._getframe().f_code.co_name, "-----")

        keypair1 = bbclib.KeyPair()
        keypair1.generate()

        pem1 = keypair1.get_private_key_in_pem()
        der1 = keypair1.get_private_key_in_der()

        keypair2 = bbclib.KeyPair()
        keypair2.mk_keyobj_from_private_key_pem(pem1)

        keypair3 = bbclib.KeyPair()
        keypair3.mk_keyobj_from_private_key_der(der1)

        privkey1 = keypair1.private_key
        pubkey1 = keypair1.public_key
        privkey2 = keypair2.private_key
        pubkey2 = keypair2.public_key
        privkey3 = keypair3.private_key
        pubkey3 = keypair3.public_key

        if isinstance(privkey1, bytes):
            assert privkey1 == privkey2
            assert privkey2 == privkey3
            assert pubkey1 == pubkey2
            assert pubkey2 == pubkey3
        else:
            assert bytes(privkey1) == bytes(privkey2)
            assert bytes(privkey2) == bytes(privkey3)
            assert bytes(pubkey1) == bytes(pubkey2)
            assert bytes(pubkey2) == bytes(pubkey3)

    def test_02_pem(self):
        print("\n-----", sys._getframe().f_code.co_name, "-----")
        pem1 = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIDSt1IOhS5ZmY6nkX/Wh7pT+Y45TmYxrwoc1pG72v387oAoGCCqGSM49\nAwEHoUQDQgAEdEsjD2i2LytHOjNxxc9PbFeqQ89aMLOfmdBbEoSOhZBukJ52EqQM\nhOdgHqyqD4hEyYxgDu3uIbKat+lEZEhb3Q==\n-----END EC PRIVATE KEY-----"
        keypair1 = bbclib.KeyPair()
        keypair1.mk_keyobj_from_private_key_pem(pem1)
        privkey1 = keypair1.private_key
        pem1_1 = keypair1.get_private_key_in_pem()
        pem1_1 = pem1_1.decode().rstrip()
        assert pem1 == pem1_1

        keypair2 = bbclib.KeyPair()
        keypair2.mk_keyobj_from_private_key(privkey1)
        pem2 = keypair2.get_private_key_in_pem()
        pem2 = pem2.decode().rstrip()
        assert pem1 == pem2

    def test_03_keyid(self):
        print("\n-----", sys._getframe().f_code.co_name, "-----")
        pem1 = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIDSt1IOhS5ZmY6nkX/Wh7pT+Y45TmYxrwoc1pG72v387oAoGCCqGSM49\nAwEHoUQDQgAEdEsjD2i2LytHOjNxxc9PbFeqQ89aMLOfmdBbEoSOhZBukJ52EqQM\nhOdgHqyqD4hEyYxgDu3uIbKat+lEZEhb3Q==\n-----END EC PRIVATE KEY-----"
        keypair1 = bbclib.KeyPair()
        keypair1.mk_keyobj_from_private_key_pem(pem1)
        keyid1 = keypair1.get_key_id()

        pubkey = keypair1.get_public_key_in_pem()
        obj = JsonWebKey.import_key(pubkey, {'kty': 'EC'})
        obj["kty"] = "EC"
        json_obj = json.dumps(obj, separators=(',', ':'), sort_keys=True)
        keyid2 = hashlib.sha256(json_obj.encode()).digest()
        assert keyid1 == keyid2

