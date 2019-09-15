Utility functions in py-bbclib version 1.5
====

py-bbclibには、トランザクションを作成するためのユーティリティ関数が用意されている。ユーティリティ関数はすべて、bbclibモジュールに含まれているため、```import bbclib```で利用できるようになる。

* [トランザクションの作成](#トランザクションの作成)
* [アセット（BBcAsset）を作成し、BBcRelationに格納する](#アセット（BBcAsset）を作成し、BBcRelationに格納する)
* [アセット（BBcAssetRaw）を作成し、BBcRelationに格納する](#アセット（BBcAssetRaw）を作成し、BBcRelationに格納する)
* [アセット（BBcAssetHash）を作成し、BBcRelationに格納する](#アセット（BBcAssetHash）を作成し、BBcRelationに格納する)
* [ポインタを作成し、BBcRelationに格納する](#ポインタを作成し、BBcRelationに格納する)
* [UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する](#UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する)
* [アセット（BBcAsset）を作成し、BBcEventに格納する](#アセット（BBcAsset）を作成し、BBcEventに格納する)
* [アセット（BBcAsset）を含むBBcRelationを作成する](#アセット（BBcAsset）を含むBBcRelationを作成する)
* [アセット（BBcAssetRaw）を含むBBcRelationを作成する](#アセット（BBcAssetRaw）を含むBBcRelationを作成する)
* [アセット（BBcAssetHash）を含むBBcRelationを作成する](#アセット（BBcAssetHash）を含むBBcRelationを作成する)
* [BBcRelationオブジェクトの中にポインタを追加する](#BBcRelationオブジェクトの中にポインタを追加する)
* [シリアライズされた署名オブジェクト単体（BBcSignature）をデシリアライズする](#シリアライズされた署名オブジェクト単体（BBcSignature）をデシリアライズする)



## トランザクションの作成

ユーティリティ関数：bbclib.make_transaction

```python
def make_transaction(event_num=0, relation_num=0, witness=False, version=2):
```

 #### 説明

BBcEvent、BBcRelation、BBcWitnessオブジェクトを含んだBBcTransactionオブジェクトを生成する。event_num、relation_numはそれぞれのオブジェクトの個数、witnessはTrueにするとBBcWitnessを含める。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
```

生成されたtxobjには、txobj.relations配列にBBcRelationオブジェクトが一つと、txobj.witnessにBBcWitnessオブジェクトが含まれている。ただし、中身はこの時点では何も無い。



## アセット（BBcAsset）を作成し、BBcRelationに格納する

ユーティリティ関数：bbclib.add_relation_asset

```python
def add_relation_asset(transaction, relation_idx, asset_group_id, user_id, asset_body=None, asset_file=None):
```

#### 説明

指定されたBBcTransactionオブジェクトの中のrelations配列の指定された要素にあるBBcRelationオブジェクトに対して、asset_group_idを設定するとともに、BBcAssetオブジェクトを新規生成して追加する。またそのBBcAssetの中身（user_id、 asset_body、asset_file）も作成する。

#### 用例

```python
bbclib.add_relation_asset(txobj,
                          relation_idx=0,
                          asset_group_id=<bytes型識別子>,
                          user_id=<bytes型識別子>,
                          asset_body=<文字列,bytes型など任意の情報>)
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].assetに新規作成したBBcAssetオブジェクトを格納する。つまり、txobj.relations[0].assetはBBcAssetオブジェクトであり、その中のuser_idとasset_bodyは引数の値を格納する。この場合はasset_fileは含まれない。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## アセット（BBcAssetRaw）を作成し、BBcRelationに格納する

ユーティリティ関数：bbclib.add_relation_asset_raw

```python
def add_relation_asset_raw(transaction, relation_idx, asset_group_id, asset_id=None, asset_body=None):
```

#### 説明

指定されたBBcTransactionオブジェクトの中のrelations配列の指定された要素にあるBBcRelationオブジェクトに対して、asset_group_idを設定するとともに、BBcAssetRawオブジェクトを新規生成して追加する。またそのBBcAssetRawの中身（asset_id、 asset_body）も作成する。

#### 用例

```python
bbclib.add_relation_asset_raw(txobj,
                              relation_idx=0,
                              asset_group_id=<bytes型識別子>,
                              asset_id=<bytes型識別子>,
                              asset_body=<文字列,bytes型など任意の情報>)
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].asset_rawに新規作成したBBcAssetRawオブジェクトを格納する。つまり、txobj.relations[0].asset_rawはBBcAssetRawオブジェクトであり、その中のasset_idとasset_bodyは引数の値を格納する。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## アセット（BBcAssetHash）を作成し、BBcRelationに格納する

ユーティリティ関数：bbclib.add_relation_asset_hash

```python
def add_relation_asset_hash(transaction, relation_idx, asset_group_id, asset_id=None, asset_body=None):
```

#### 説明

指定されたBBcTransactionオブジェクトの中のrelations配列の指定された要素にあるBBcRelationオブジェクトに対して、asset_group_idを設定するとともに、BBcAssetHashオブジェクトを新規生成して追加する。またそのBBcAssetHashの中身（asset_idの配列）も作成する。

#### 用例

```python
bbclib.add_relation_asset_hash(txobj,
                               relation_idx=0,
                               asset_group_id=<bytes型識別子>,
                               asset_ids=[<bytes型識別子>,<bytes型識別子>,,,])
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].asset_hashに新規作成したBBcAssetHashオブジェクトを格納する。つまり、txobj.relations[0].asset_hashはBBcAssetHashオブジェクトであり、その中のasset_ids配列に引数で与えた配列を格納する。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## ポインタを作成し、BBcRelationに格納する

ユーティリティ関数：bbclib.add_relation_pointer

```python
def add_relation_pointer(transaction, relation_idx, ref_transaction_id=None, ref_asset_id=None):
```

#### 説明

指定されたBBcTransactionオブジェクトの中のrelations配列の指定された要素にあるBBcRelationオブジェクトに対して、BBcPointerオブジェクトを新規生成して追加する。またそのBBcPointerの中身（ref_transaction_id、 ref_asset_id）も作成する。

#### 用例

```python
bbclib.add_relation_pointer(txobj,
                            relation_idx=0,
                            ref_transaction_id=some_txobj.digest())
```

txobj.relations[0]のBBcRelationオブジェクトに、BBcPointerオブジェクトを新規生成して追加する。つまり、txobj.relations[0].pointers[0]にBBcPointerオブジェクトがappendされる。またそのtransaction_id に引数の値を格納する。この場合はasset_idは設置されずNoneになる。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する

ユーティリティ関数：bbclib.add_reference_to_transaction

```python
def add_reference_to_transaction(transaction, asset_group_id, ref_transaction_obj, event_index_in_ref):
```

#### 説明

指定されたBBcTransactionオブジェクトに、BBcReferenceオブジェクトを新規作成して追加する。そのオブジェクトのasset_group_idを指定するとともに、UTXOの出力となるBBcEventおよびそれを含むトランザクションも指定する。

#### 用例

```python
bbclib.add_reference_to_transaction(txobj,
                                    asset_group_id=<bytes型識別子>,
				                            ref_transaction_obj=some_txobj
                                    event_index_in_ref=0)
```

txobj.references[0]に、BBcReferenceオブジェクトを新規生成して追加する。またasset_group_idも設定する。さらに、UTXOの出力となるBBcEventオブジェクトとして、some_txobjというBBcTransactionおぶじぇくとの1番目のBBcEventオブジェクト（つまり、txobj.events[0]）を指定する。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## アセット（BBcAsset）を作成し、BBcEventに格納する

ユーティリティ関数：bbclib.add_event_asset

```python
def add_event_asset(transaction, event_idx, asset_group_id, user_id, asset_body=None, asset_file=None):
```

#### 説明

指定されたBBcTransactionオブジェクトの中のevents配列の指定された要素にあるBBcEventオブジェクトに対して、asset_group_idを設定するとともに、BBcAssetオブジェクトを新規生成して追加する。またそのBBcAssetの中身（user_id、 asset_body、asset_file）も作成する。

#### 用例

```python
bbclib.add_event_asset(txobj,
                       event_idx=0,
                       asset_group_id=<bytes型識別子>,
                       user_id=<bytes型識別子>,
                       asset_body=<文字列,bytes型など任意の情報>)
```

txobj.events[0]のBBcEventオブジェクトに、asset_group_idを設定し、txobj.events[0].assetに新規作成したBBcAssetオブジェクトを格納する。つまり、txobj.events[0].assetはBBcAssetオブジェクトであり、その中のuser_idとasset_bodyは引数の値を格納する。この場合はasset_fileは含まれない。また、BBcEventにはmandatory_approversやoption_approversを指定する必要があるが、このユーティリティ関数にはその機能はない。

戻り値はなく、第１引数のtxobjは参照渡しなので、そのオブジェクト自体に追加される。



## アセット（BBcAsset）を含むBBcRelationを作成する

ユーティリティ関数：bbclib.make_relation_with_asset

```python
def make_relation_with_asset(asset_group_id, user_id, asset_body=None, asset_file=None):
```

#### 説明

BBcRelationオブジェクトを作成し、asset_group_idを設定するとともに、BBcAssetオブジェクトを新規生成してBBcRelationオブジェクトの中に追加する。またそのBBcAssetの中身（user_id、 asset_body、asset_file）も作成する。

#### 用例

```python
relation_obj = bbclib.make_relation_with_asset(
                                               asset_group_id=<bytes型識別子>,
                                               user_id=<bytes型識別子>,
                                               asset_body=<文字列,bytes型など任意の情報>)
```

戻り値のrelation_objは、新規作成されたBBcRelationオブジェクトであり、relation_obj.asset_group_idとrelation_obj.assetが設定されている。relation_obj.assetは新規作成されたBBcAssetオブジェクトであり、その中のuser_idとasset_bodyは引数の値を格納する。この場合はasset_fileは含まれない。



## アセット（BBcAssetRaw）を含むBBcRelationを作成する

ユーティリティ関数：bbclib.make_relation_with_asset_raw

```python
def make_relation_with_asset_raw(asset_group_id, user_id, asset_id=None, asset_body=None):
```

#### 説明

BBcRelationオブジェクトを作成し、asset_group_idを設定するとともに、BBcAssetRawオブジェクトを新規生成してBBcRelationオブジェクトの中に追加する。またそのBBcAssetRawの中身（asset_id、 asset_body）も作成する。

#### 用例

```python
relation_obj = bbclib.make_relation_with_asset_raw(
                                               asset_group_id=<bytes型識別子>,
                                               asset_id=<bytes型識別子>,
                                               asset_body=<文字列,bytes型など任意の情報>)
```

戻り値のrelation_objは、新規作成されたBBcRelationオブジェクトであり、relation_obj.asset_group_idとrelation_obj.asset_rawが設定されている。relation_obj.asset_rawは新規作成されたBBcAssetRawオブジェクトであり、その中のasset_idとasset_bodyは引数の値を格納する。



## アセット（BBcAssetHash）を含むBBcRelationを作成する

ユーティリティ関数：bbclib.make_relation_with_asset_hash

```python
def make_relation_with_asset_hash(asset_group_id, asset_id=None, asset_body=None):
```

#### 説明

BBcRelationオブジェクトを作成し、asset_group_idを設定するとともに、BBcAssetHashオブジェクトを新規生成してBBcRelationオブジェクトの中に追加する。またそのBBcAssetHashの中身（asset_idの配列）も作成する。

#### 用例

```python
relation_obj = bbclib.make_relation_with_asset_raw(
                                               asset_group_id=<bytes型識別子>,
                                               asset_ids=[<bytes型識別子>,<bytes型識別子>,,,]
```

戻り値のrelation_objは、新規作成されたBBcRelationオブジェクトであり、relation_obj.asset_group_idとrelation_obj.asset_raw_hashが設定されている。relation_obj.asset_hashは新規作成されたBBcAssetHashオブジェクトであり、その中のasset_idsに引数で指定されたリストを格納する。



## BBcRelationオブジェクトの中にポインタを追加する

ユーティリティ関数：bbclib.add_pointer_in_relation

```python
def add_pointer_in_relation(relation, ref_transaction_id=None, ref_asset_id=None):
```

#### 説明

指定されたBBcRelationオブジェクトの中のpointers配列に、BBcPointerオブジェクトを新規生成して追加する。またそのBBcPointerの中身（ref_transaction_id、 ref_asset_id）も作成する。

#### 用例

```python
bbclib.add_relation_pointer(relation_obj,
                            ref_transaction_id=some_txobj.digest(),
                            ref_asset_id=some_txobj.relations[0].asset.asset_id)
```

与えられたBBcRelationオブジェクト（relation_obj）に、BBcPointerオブジェクトを新規生成して追加する。またそのBBcPointerのtransaction_id とasset_idにそれぞれ引数の値を格納する。この場合はsome_txobjがBBcRelationオブジェクトを含んでいることを想定している（some_txobj.relations[0]の部分）。

戻り値はなく、第１引数のrelation_objは参照渡しなので、そのオブジェクト自体に追加される。



## シリアライズされた署名オブジェクト単体（BBcSignature）をデシリアライズする

ユーティリティ関数：bbclib.recover_signature_object

```python
def recover_signature_object(data):
```

#### 説明

シリアライズされた署名オブジェクト単体（BBcSignature）をデシリアライズする。マルチシグを実施したいときなどに署名だけを相手から送ってもらう場合の利用を想定している。

#### 用例

```python
some_signature = BBcSignature()
#...（署名に関する処理は記載を省略）...
sig_data = some_signature.pack()

recovered_sig = bbclib.recover_signature_object(sig_data)
```

別のユーザによって作られたBBcSignatureオブジェクトをシリアライズ（sig_data）して相手に送付したり、DBに格納したりすることを想定している。デシリアライズして得られたrecovered_sigは元のsome_signatureと同じものである。