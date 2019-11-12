# -*- coding: utf-8 -*-
import sys
sys.path.extend(["../"])
from bbclib import KeyPair, BBcTransaction
import bbclib

user_id1 = bbclib.get_new_id("user_id_test1")
user_id2 = bbclib.get_new_id("user_id_test2")
domain_id = bbclib.get_new_id("testdomain")
asset_group_id1 = bbclib.get_new_id("asset_group_1")
asset_group_id2 = bbclib.get_new_id("asset_group_2")
pem1 = ""
pem2 = ""

txdata_list = list()
id_conf = {
    "transaction_id": 24,
    "asset_group_id": 8,
    "user_id": 6,
    "asset_id": 16,
    "nonce": 9
}


def make_transactions(id_len_conf=None, idlen=None, no_pubkey=False):
    keypair1 = KeyPair()
    keypair1.generate()
    keypair2 = KeyPair()
    keypair2.generate()

    global pem1, pem2
    pem1 = keypair1.get_private_key_in_pem()
    pem2 = keypair2.get_private_key_in_pem()

    transactions = list()
    if id_len_conf is not None:
        bbclib.configure_id_length(id_len_conf)
    elif idlen is not None:
        bbclib.configure_id_length_all(idlen)

    txobj = bbclib.make_transaction(event_num=1, relation_num=1, witness=True)
    transactions.append(txobj)
    txobj.relations[0].set_asset_group(asset_group_id1).create_asset(user_id=user_id1, asset_body=b'relation:asset_0-0')
    txobj.events[0].set_asset_group(asset_group_id1).create_asset(user_id=user_id1, asset_body=b'event:asset_0-0').add_mandatory_approver(user_id1)
    transactions[0].add_witness(user_id1)
    transactions[0].add_signature(user_id=user_id1, keypair=keypair1)

    for i in range(1, 20):
        k = i - 1
        txobj = bbclib.make_transaction(event_num=1, relation_num=4, witness=True)
        txobj.relations[0].set_asset_group(asset_group_id1)\
            .create_asset(user_id=user_id1, asset_body=b'relation:asset_1-%d' % i) \
            .create_pointer(transaction_id=transactions[k].transaction_id, asset_id=transactions[k].relations[0].asset.asset_id)
        txobj.relations[1].set_asset_group(asset_group_id2) \
            .create_asset(user_id=user_id2, asset_body=b'relation:asset_2-%d' % i) \
            .create_pointer(transaction_id=transactions[k].transaction_id, asset_id=transactions[k].relations[0].asset.asset_id) \
            .create_pointer(transaction_id=transactions[0].transaction_id, asset_id=transactions[0].relations[0].asset.asset_id)
        txobj.events[0].set_asset_group(asset_group_id1)\
            .create_asset(user_id=user_id2, asset_body=b'event:asset_3-%d' % i).add_mandatory_approver(user_id1)

        ash = [bbclib.get_new_id("assethash%d" % i)[:bbclib.id_length_conf["asset_id"]] for i in range(5)]
        txobj.relations[2].set_asset_group(asset_group_id1)\
            .create_asset_raw(asset_id=ash[0], asset_body=b'relation:asset_4-%d' % i) \
            .create_pointer(transaction_id=transactions[0].transaction_id, asset_id=transactions[0].relations[0].asset.asset_id) \
            .create_pointer(transaction_id=transactions[0].transaction_id, asset_id=None)
        txobj.relations[3].set_asset_group(asset_group_id2)\
            .create_asset_hash(asset_ids=ash[1:])\
            .create_pointer(transaction_id=transactions[0].transaction_id, asset_id=transactions[0].relations[0].asset.asset_id)

        txobj.create_reference(asset_group_id1, ref_transaction=transactions[i-1], event_index_in_ref=0)
        txobj.create_cross_ref(transactions[0].transaction_id, domain_id=domain_id)

        txobj.add_witness(user_id1)
        txobj.add_witness(user_id2)

        txobj.add_signature(user_id1, keypair=keypair1, no_pubkey=no_pubkey)
        txobj.add_signature(user_id2, keypair=keypair2, no_pubkey=no_pubkey)
        transactions.append(txobj)

    return transactions


class TestBBcLib(object):

    def test_01_create(self):
        print("\n-----", sys._getframe().f_code.co_name, "-----")
        txobjs = make_transactions(id_len_conf=id_conf)

        for txobj in txobjs:
            txdata = bbclib.serialize(txobj)
            txdata_list.append(txdata)

    def test_02_verify(self):
        print("\n-----", sys._getframe().f_code.co_name, "-----")

        keypair1 = bbclib.KeyPair()
        keypair1.mk_keyobj_from_private_key_pem(pem1)
        keypair2 = bbclib.KeyPair()
        keypair2.mk_keyobj_from_private_key_pem(pem2)

        bbclib.configure_id_length_all(32)
        transactions = list()
        txids = list()
        for txdata in txdata_list:
            txobj, _ = bbclib.deserialize(txdata)
            transactions.append(txobj)
            txids.append(txobj.transaction_id)

        for idx in range(len(transactions)):
            txobj = transactions[idx]
            if idx % 20 == 0:
                assert len(txobj.transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations) == 1
                assert len(txobj.events) == 1
                assert txobj.transaction_id == txids[idx]
                assert txobj.relations[0].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.relations[0].asset.user_id == user_id1[:id_conf["user_id"]]
                assert txobj.relations[0].asset.asset_body == b'relation:asset_0-0'
                assert len(txobj.relations[0].asset.nonce) == id_conf["nonce"]
                assert txobj.events[0].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.events[0].mandatory_approvers[0] == user_id1[:id_conf["user_id"]]
                assert txobj.events[0].asset.user_id == user_id1[:id_conf["user_id"]]
                assert txobj.events[0].asset.asset_body == b'event:asset_0-0'
                assert len(txobj.events[0].asset.nonce) == id_conf["nonce"]
                assert len(txobj.witness.user_ids) == 1
                assert len(txobj.witness.sig_indices) == 1
                assert len(txobj.signatures) == 1
                if idx < 20:
                    assert txobj.signatures[0].verify(txobj.digest())
                else:
                    #print("no pubkey")
                    pass

            else:
                assert len(txobj.transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations) == 4
                assert len(txobj.relations[0].pointers) == 1
                assert len(txobj.relations[1].pointers) == 2
                assert len(txobj.events) == 1
                assert len(txobj.references) == 1
                assert txobj.relations[0].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.relations[0].asset.user_id == user_id1[:id_conf["user_id"]]
                assert txobj.relations[0].asset.asset_body == b'relation:asset_1-%d' % (idx % 20)
                assert len(txobj.relations[0].asset.nonce) == id_conf["nonce"]
                assert len(txobj.relations[0].pointers[0].transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations[0].pointers[0].asset_id) == id_conf["asset_id"]
                assert txobj.relations[0].pointers[0].transaction_id == transactions[idx-1].transaction_id
                assert txobj.relations[0].pointers[0].asset_id == transactions[idx-1].relations[0].asset.asset_id
                assert txobj.relations[1].asset_group_id == asset_group_id2[:id_conf["asset_group_id"]]
                assert txobj.relations[1].asset.user_id == user_id2[:id_conf["user_id"]]
                assert txobj.relations[1].asset.asset_body == b'relation:asset_2-%d' % (idx % 20)
                assert len(txobj.relations[1].asset.nonce) == id_conf["nonce"]
                assert len(txobj.relations[1].pointers[0].transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations[1].pointers[0].asset_id) == id_conf["asset_id"]
                assert txobj.relations[1].pointers[0].transaction_id == transactions[idx-1].transaction_id
                assert txobj.relations[1].pointers[0].asset_id == transactions[idx-1].relations[0].asset.asset_id
                assert len(txobj.relations[1].pointers[1].transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations[1].pointers[1].asset_id) == id_conf["asset_id"]

                assert txobj.relations[2].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.relations[2].asset_raw.asset_body == b'relation:asset_4-%d' % (idx % 20)
                assert len(txobj.relations[2].pointers[0].transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations[2].pointers[0].asset_id) == id_conf["asset_id"]
                assert len(txobj.relations[2].pointers[1].transaction_id) == id_conf["transaction_id"]
                assert txobj.relations[2].pointers[1].asset_id is None

                assert txobj.relations[3].asset_group_id == asset_group_id2[:id_conf["asset_group_id"]]
                assert len(txobj.relations[3].asset_hash.asset_ids) == 4
                assert len(txobj.relations[3].pointers[0].transaction_id) == id_conf["transaction_id"]
                assert len(txobj.relations[3].pointers[0].asset_id) == id_conf["asset_id"]

                if idx < 20:
                    assert txobj.relations[1].pointers[1].transaction_id == transactions[0].transaction_id
                    assert txobj.relations[1].pointers[1].asset_id == transactions[0].relations[0].asset.asset_id
                    assert txobj.relations[2].pointers[0].transaction_id == transactions[0].transaction_id
                    assert txobj.relations[2].pointers[0].asset_id == transactions[0].relations[0].asset.asset_id
                    assert txobj.relations[2].pointers[1].transaction_id == transactions[0].transaction_id
                    assert txobj.relations[3].pointers[0].transaction_id == transactions[0].transaction_id
                    assert txobj.relations[3].pointers[0].asset_id == transactions[0].relations[0].asset.asset_id
                else:
                    assert txobj.relations[1].pointers[1].transaction_id == transactions[20].transaction_id
                    assert txobj.relations[1].pointers[1].asset_id == transactions[20].relations[0].asset.asset_id
                    assert txobj.relations[2].pointers[0].transaction_id == transactions[20].transaction_id
                    assert txobj.relations[2].pointers[0].asset_id == transactions[20].relations[0].asset.asset_id
                    assert txobj.relations[2].pointers[1].transaction_id == transactions[20].transaction_id
                    assert txobj.relations[3].pointers[0].transaction_id == transactions[20].transaction_id
                    assert txobj.relations[3].pointers[0].asset_id == transactions[20].relations[0].asset.asset_id

                assert txobj.events[0].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.events[0].mandatory_approvers[0] == user_id1[:id_conf["user_id"]]
                assert txobj.events[0].asset.user_id == user_id2[:id_conf["user_id"]]
                assert txobj.events[0].asset.asset_body == b'event:asset_3-%d' % (idx % 20)
                assert len(txobj.events[0].asset.nonce) == id_conf["nonce"]
                assert txobj.references[0].asset_group_id == asset_group_id1[:id_conf["asset_group_id"]]
                assert txobj.references[0].event_index_in_ref == 0
                assert len(txobj.references[0].sig_indices) == 1
                assert txobj.cross_ref.domain_id == domain_id
                if idx < 20:
                    assert txobj.cross_ref.transaction_id == transactions[0].transaction_id
                else:
                    assert txobj.cross_ref.transaction_id == transactions[20].transaction_id
                assert len(txobj.witness.user_ids) == 2
                assert len(txobj.witness.sig_indices) == 2
                assert len(txobj.signatures) == 2
                if txobj.signatures[0].pubkey is None:
                    pass
                else:
                    assert txobj.signatures[0].verify(txobj.digest())
                if txobj.signatures[1].pubkey is None:
                    pass
                else:
                    assert txobj.signatures[1].verify(txobj.digest())

