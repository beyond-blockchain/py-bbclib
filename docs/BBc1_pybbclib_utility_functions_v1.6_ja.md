Utility functions in py-bbclib version 1.6
====

py-bbclib v1.6で、トランザクション作成用のメソッドが追加された。v1.6以前はユーティリティメソッド（bbclib_utils.py）を利用していたが、v1.6からは、トランザクションオブジェクト自体にユーティリティメソッドが含まれるようになり、より直感的にトランザクションを構築できるようになった。

* [トランザクションの作成](#トランザクションの作成)
* [BBcRelationにアセット(BBcAsset)を格納する](#BBcRelationにアセット(BBcAsset)を格納する)
* [BBcRelationにアセット（BBcAssetRaw）を格納する](#BBcRelationにアセット（BBcAssetRaw）を格納する)
* [BBcRelationにアセット（BBcAssetHash）を格納する](#BBcRelationにアセット（BBcAssetHash）を格納する)
* [ポインタを作成し、BBcRelationに格納する](#ポインタを作成し、BBcRelationに格納する)
* [UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する](#UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する)
* [BBcEventを準備し、アセット（BBcAsset）を格納する](#BBcEventを準備し、アセット（BBcAsset）を格納する)
* [BBcEventにapproverを追加する](#BBcEventにapproverを追加する)
* [署名する（BBcWitnessとBBcSignature）](#署名する（BBcWitnessとBBcSignature）)
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



## BBcRelationにアセット(BBcAsset)を格納する

```python
def set_asset_group(self, asset_group_id)
def create_asset(self, user_id, asset_body=None, asset_file=None)
```

#### 説明

BBcRelationオブジェクトに対して、asset_group_idを設定したり（set_asset_group）、BBcAssetオブジェクトを新規生成して追加する。またそのBBcAssetの中身（user_id、 asset_body、asset_file）も作成する（create_asset）。なお、これらの戻り値はすべて呼び出し元のBBcRelationオブジェクトである。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.relations[0] \
    .set_asset_group(<bytes型識別子>) \
    .create_asset(user_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>)
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].assetに新規作成したBBcAssetオブジェクトを格納する。この例ではアセットにははasset_fileは含まれない。

set_asset_group()およびcreate_asset()はいずれも戻り値がrelations[0]のオブジェクトであるため、メソッドチェーンで記述可能であるが、もちろん、以下のようにset_asset_group()およびcreate_asset()を分けてもよい。以降本資料では、メソッドチェーンの用例で記載する。

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.relations[0].set_asset_group(<bytes型識別子>)
txobj.relations[0].create_asset(user_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>)
```



## BBcRelationにアセット（BBcAssetRaw）を格納する

```python
def create_asset(self, asset_id, asset_body=None)
```

#### 説明

BBcRelationオブジェクトに対して、BBcAssetRawオブジェクトを新規生成して追加する。またそのBBcAssetRawの中身（asset_id、 asset_body）も作成する。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.relations[0] \
   .set_asset_group(<bytes型識別子>) \
   .create_asset_raw(asset_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>)
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].asset_rawに新規作成したBBcAssetRawオブジェクトを格納する。



## BBcRelationにアセット（BBcAssetHash）を格納する

```python
def create_asset_hash(self, asset_ids)
```

#### 説明

BBcRelationオブジェクトに対して、BBcAssetHashオブジェクトを新規生成して追加する。またそのBBcAssetHashの中身（asset_idの配列）も作成する。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.relations[0] \
   .set_asset_group(<bytes型識別子>) \
   .create_asset_hash(asset_ids=[<bytes型識別子>,<bytes型識別子>,,,])
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].asset_hashに新規作成したBBcAssetHashオブジェクトを格納する。



## ポインタを作成し、BBcRelationに格納する

```python
def create_pointer(self, transaction_id, asset_id=None):
```

#### 説明

BBcRelationオブジェクトに対して、BBcPointerオブジェクトを新規生成して追加する。またそのBBcPointerの中身（transaction_id、 asset_id）も作成する。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.relations[0] \
    .set_asset_group(<bytes型識別子>) \
    .create_asset(user_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>) \
    .create_pointer(transaction_id=<bytes型識別子>, asset_id=<bytes型識別子>)
```

txobj.relations[0]のBBcRelationオブジェクトに、asset_group_idを設定し、txobj.relations[0].assetに新規作成したBBcAssetオブジェクトを格納する。さらに、BBcPointerオブジェクトを新規生成して追加する。つまり、txobj.relations[0].pointers[0]にBBcPointerオブジェクトがappendされる。

create_pointer()の戻り値も呼び出し元のBBcRelationオブジェクトであるため、他と同じようにメソッドチェーンに含めることができる。



## UTXOのリファレンス（BBcReference）を作成し、トランザクションに追加する

```python
def create_reference(self, asset_group_id, ref_transaction_obj, event_index_in_ref)
```

#### 説明

BBcTransactionオブジェクトに、BBcReferenceオブジェクトを新規作成して追加する。そのオブジェクトのasset_group_idを指定するとともに、UTXOの出力となるBBcEventおよびそれを含むトランザクションも指定する。

#### 用例

```python
txobj = bbclib.make_transaction(event_num=1, witness=True)
txobj.create_reference(asset_group_id=<bytes型識別子>,
				               ref_transaction_obj=some_txobj
                       event_index_in_ref=0)
```

txobj.references[0]に、BBcReferenceオブジェクトを新規生成して追加する。またasset_group_idも設定する。さらに、UTXOの出力となるBBcEventオブジェクトとして、some_txobjというBBcTransactionおぶじぇくとの1番目のBBcEventオブジェクト（つまり、txobj.events[0]）を指定する。なお、この例ではmake_transaction()でBBcRelationオブジェクトを1つとBBcWitnessオブジェクトを生成しているが、BBcReferenceはmake_transaction()メソッドの対象外であるため、create_reference()を用いて生成する。

create_reference()の戻り値は呼び出し元のtxobjである。



## BBcEventを準備し、アセット（BBcAsset）を格納する

```python
def set_asset_group(self, asset_group_id)
def add_reference_index(self, index)
def create_asset(self, user_id, asset_body=None, asset_file=None)
```

#### 説明

BBcEventオブジェクトに対して、asset_group_idの設定、参照先BBcReferenceオブジェクトの要素番号の指定、BBcAssetオブジェクトの新規生成を行う。この考え方はBBcRelationオブジェクトのset_asset_group()とcreate_asset()と全く同じである。なお、BBcEventにはv1.6現在ではBBcAssetRawとBBcAssetHashが定義されていないため、create_asset_raw()やcreate_asset_hash()は定義されていない。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.events[0] \
    .set_asset_group(<bytes型識別子>) \
    .add_reference_index(0) \
    .create_asset(user_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>)
```

txobj.events[0]のBBcEventオブジェクトに、asset_group_idおよび参照先BBcReferenceオブジェクトを指定する。また、txobj.events[0].assetには新規作成したBBcAssetオブジェクトを格納する。つまり、txobj.events[0].assetはBBcAssetオブジェクトであり、その中のuser_idとasset_bodyは引数の値を格納する。この場合はasset_fileは含まれない。なお、add_reference_index()はtxobjにBBcReferenceオブジェクトが含まれない場合はコールする必要はない。

これらのメソッドの戻り値は、呼び出し元のBBcEventオブジェクトなので、メソッドチェーン形式を用いることができる。



## BBcEventにapproverを追加する

```python
def add_mandatory_approver(self, approver)
def add_option_approver(self, approver)
def set_option_parameter(self, numerator, denominator)
```

#### 説明

BBcEventオブジェクトに対して、mandatory_approver、option_approverを追加する。また、set_option_parameter()で必要署名数(=numerator)と承認者候補数(=denominator)のオプション条件を設定する。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
txobj.events[0] \
    .set_asset_group(<bytes型識別子>) \
    .add_reference_index(0) \
    .create_asset(user_id=<bytes型識別子>, asset_body=<文字列,bytes型など任意の情報>) \
    .add_mandatory_approver(<bytes型識別子>) \
    .add_mandatory_approver(<bytes型識別子>) \
    .set_option_parameter(numerator=1, denominator=3) \
    .add_option_approver(<bytes型識別子>) \
    .add_option_approver(<bytes型識別子>) \
    .add_option_approver(<bytes型識別子>)
```

前述の用例にさらにadd_mandatory_approver()、add_option_approver()、set_option_parameter()を追加した。この用例では、必須の署名者を2人、オプションの署名者を3人（うち1名の署名が必須）という条件を設定している。

これらのメソッドの戻り値はすべて呼び出し元のBBcEventオブジェクトであり、メソッドチェーン形式で記述できる。



## 署名する（BBcWitnessとBBcSignature）

```python
def add_witness(self, user_id)
def add_signature(self, key_type=None, private_key=None, public_key=None,
                  keypair=None, no_pubkey=False)
```

#### 説明

BBcWitnessオブジェクトに署名予定のuser_idを登録したり(add_witness)、BBcTransactionオブジェクトに署名を追加する(add_signature)。

#### 用例

```python
txobj = bbclib.make_transaction(relation_num=1, witness=True)
..中略

txobj \
   .add_witness(user_id=<bytes型識別子1>) \
   .add_witness(user_id=<bytes型識別子2>)

txobj \
  .add_signature(user_id=<bytes型識別子1>, keypair=<KeyPairオブジェクト>) \
  .add_signature(user_id=<bytes型識別子2>, keypair=<KeyPairオブジェクト>)
```

add_witness()で署名するユーザのuser_idを登録している。BBcWitnessまで作成が完了したのちに、add_signature()で署名オブジェクトをトランザクションに付加する。なお、add_witness()およびadd_signature()の戻り値は呼び出し元のtxobj自身であるため、例示したようにメソッドチェーン形式で記述できる。



## シリアライズされた署名オブジェクト単体（BBcSignature）をデシリアライズする

ユーティリティ関数：bbclib.recover_signature_object

```python
def recover_signature_object(data)
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