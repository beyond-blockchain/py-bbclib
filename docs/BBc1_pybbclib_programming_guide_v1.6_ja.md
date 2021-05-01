Programming guide for py-bbclib version 1.6
====

py-bbclibはBBc-1のトランザクションのデータ構造を定義するモジュールであり、BBc-1の中で最も重要な役割をもつ。このドキュメントでは、py-bbclibの利用方法についてまとめ、後半では事例集を載せる。

なお、このリポジトリはbbc1リポジトリからも参照されるが、BBc-1のアプリケーション開発のための解説はbbc1リポジトリ内の[docs/BBc1_programming_guide_v1.3_ja.md](https://github.com/beyond-blockchain/bbc1/tree/develop/docs)を参照されたい。

v1.6へのアップデートではいくつかのAPIが追加され、トランザクションの生成をより直観的に行えるようにした。具体的なコーディング方法は、[docs/BBc1_pybbclib_utility_functions_v1.6_ja.md](../docs/BBc1_pybbclib_utility_functions_v1.6_ja.md)を参照されたい。なお、後方互換性は保たれており、v1.5までのコードもそのまま動作する。




# トランザクションのライフサイクル
BBc-1におけるトランザクションは以下のようなライフサイクルを持つ。

* BBcTransactionクラスのオブジェクトを作る
* BBcTransactionオブジェクトをシリアライズ（バイナリ化）して、データベースやストレージに保存したり、他のユーザに送付する
* 受け取ったシリアライズされたをデシリアライズして、BBcTransactionオブジェクトに復元し、署名を検証する
* BBcTransactionオブジェクトに含まれる情報（BBcAssetなど）を利用する

シリアライズやデシリアライズについては、[BBc1_data_format_ja.md](./BBc1_data_format_ja.md)に解説している。本ドキュメントでは、BBcTransactionクラスのオブジェクトの生成や署名検証の方法について解説する。



# BBcTransactionオブジェクトの構築

BBc-1のトランザクション（すなわちBBcTransactionオブジェクト）は、アセットデータおよび他のトランザクションへのポインタを保持し、デジタル署名によって保護される。

BBcTransactionオブジェクトを生成するためには、まずIDの長さの設定と、鍵ペアオブジェクト(KeyPairクラスのオブジェクト)の生成を行う。

### IDの長さの設定

BBcTransactionオブジェクトに含まれる[各種ID](./BBc1_IDs_ja.md)は、デフォルトではすべて256bit (=32byte)の長さを持つ。トランザクションのデータサイズを圧縮したい場合、IDの値が衝突しないと確信できるなら、長さを短縮しても実用上問題ない。v1.4以降では、IDの種別ごとに長さをバイト単位で設定することが可能である。

IDの長さに関する情報は、bbc1/bbclib.pyの中で保持している。下記のようにすることで、IDの長さを変更できる。一度変更すると、次に変更する前でその設定が引き継がれる。

```python
from bbclib import configure_id_length

id_length = {
  "transaction_id": 24,
  "asset_group_id": 6,
  "user_id": 8,
  "asset_id": 16,
  "nonce": 9
}
configure_id_length(id_len_conf)
```

上記の例では、transaction_idの長さを24バイト、asset_group_idの長さを6バイト、user_idの長さを6バイト、asset_idの長さを16バイト、BBcAssetに含まれる乱数値Nonceの長さを9バイトに設定している。

また、全て同じ長さに設定したい場合はconfigure_id_length_all()というメソッドを使うこともできる。下記は、すべてのID（およびNonce）の長さを16バイトに設定する例である。

```python
from bbclib import configure_id_length_all

configure_id_length_all(16)
```



### 鍵ペアオブジェクトの生成

トランザクションに署名したりBBcSignatureに公開鍵を格納するために、BBcTransactionオブジェクト鍵ペアを登録する必要がある。その鍵ペアは、新規に生成する場合と、既存の鍵ペアを利用する場合の2通りがある。

新規に鍵ペアを生成する方法は以下の通りである。

```python
from bbclib import KeyPair

keyPair = KeyPair()
keyPair.generate()
```

この結果、keyPairの中に秘密鍵と公開鍵が生成される。BBcTransactionにはこのkeyPairを渡せば良い。

また、このkeyPairの中の秘密鍵と公開鍵は、PEM形式、DER形式、またはナイーブなバイナリ形式（公開鍵はこの形でBBcSignatureに格納される)でエクスポートすることができる。

```python
privateKey_pem = keyPair.get_private_key_in_pem()
publicKey_pem = keyPair.get_public_key_in_pem()

privateKey_der = keyPair.get_private_key_in_der()
privateKey_der = keyPair.get_private_key_in_der()

privateKey_naive = keyPair.private_key
publicKey_naive = keyPair.public_key
```

エクスポートされた鍵をファイルやデータベースに保存しておき、それを以下のようにしてインポートすることで同じ鍵ペアをいつでも再生できる。

```python
from bbclib import KeyPair

keyPair = KeyPair()
keyPair.generate()
privateKey_pem = keyPair.get_private_key_in_pem()
// privateKey_pemをファイルに保存

...

// ファイルからprivateKey_pemを読み込む
keyPair2 = KeyPair()
keyPair2.mk_keyobj_from_private_key_pem(privateKey_pem)
```

keyPair2は、もとのkeyPairと同じ内容である。なお、鍵ペアオブジェクトの再生には、秘密鍵だけを与えればよい（公開鍵は秘密鍵から計算できるため）。上記の例は、PEM形式の鍵から再生する方法だが、この他にも、DER形式の鍵から再生するためのmk_keyobj_from_private_key()と、ナイーブなバイナリ形式から再生するためのmk_keyobj_from_private_key()も用意されている。

```python
keyPair2.mk_keyobj_from_private_key(privateKey_der)
keyPair2.mk_keyobj_from_private_key(privateKey_naive)
```

また、PEM形式の公開鍵証明書と秘密鍵のペアをインポートして鍵ペアオブジェクトを再生することもできる。下記では、公開鍵証明書(publicKey_cert_x509)と秘密鍵(privateKey_pem)を用いている。このimport_publickey_cert_pem()関数は、証明書の正しさも検証し、不正であればresult = Falseを返す。

```python
keyPair3 = KeyPair()
result = keyPair3.import_publickey_cert_pem(publicKey_cert_x509, privateKey_pem)
```



### BBcTransactionオブジェクトの生成

BBcTransactionオブジェクトを生成し、その中身に情報を追加していくことで、トランザクションを作ることができる。BBcTransactionクラスなどを直接インスタンス化して作り上げることも可能だが、ユーティリティメソッドを使うことで作成手順を減らすことができる。ここでは、v1.6で導入されたメソッドを用いた方法を紹介する。以下に例を示す。

```python
import bbclib

keyPair_1 = bbclib.KeyPair()  #1
keyPair_1.genarate()          #1

asset_group_1 = bbclib.get_new_id("asset_group_id for testing") #1
user_1 = bbclib.get_new_id("user x") #1

transaction1 = bbclib.make_transaction(relation_num=1, witness=True)  #2

transaction1.relations[0]\
   .set_asset_group(asset_group_1) \   #3
   .create_asset(user_id=user_1, asset_body=b'some information') #4

transaction1.add_witness(user_1)   # 5

txobj.add_signature(user_id=user_1, keypair=keyPair_1) #6
```

まず、上記#1では、鍵ペアを作成したり、トランザクション内で用いるIDを生成している。これらは単なるサンプルであるため、適当な値になっている。

そして、#2で必要なパーツ（この例ではBBcRelationとBBcWitnessオブジェクト）を含んだBBcTransactionオブジェクトが生成される。データ構造は[BBc-1_transaction_data_ja.md](./BBc-1_transaction_data_ja.md)を参照されたい。上記のようにして「素のトランザクション」を生成した時点ではヘッダ情報（タイムスタンプなど）しか含まれていない。そのあと、様々なパーツを追加していく必要がある。

つぎに#3にてBBcRelationオブジェクトにasset_group_idをセットし、さらに#4でBBcAssetオブジェクトを#4で追加している。set_asset_group()やcreate_asset()などは操作対象のBBcRelationオブジェクト自身を返すので、メソッドチェーン形式で記述できる。

最後の#5では、署名する予定のユーザのユーザIDをBBcWitnessオブジェクトに登録している。

ここまでで、BBcTransactionオブジェクトの本体が完成したことになる。最後に#6でuser_1の署名を付与すれば全体が完成する。この後、このオブジェクトをシリアライズすれば、それを保存したり他へ送信することができるようになる。



### BBcTransactionオブジェクト生成（ポインタを含める場合）

前節の例は、他のトランザクションと何の関係も持たない単独のトランザクションを生成する例だった。本節ではBBcPointerを含めることで、他のトランザクションとの関係性を持たせる例を紹介する。なお、関係を持たせるトランザクションは前節で生成したtransaction1とする。

```python
import bbclib

asset_group_1 = bbclib.get_new_id("asset_group_id for testing")
user_1 = bbclib.get_new_id("user x")
transaction_id_1 = transaction1.transaction_id   # 1
asset_id_1 = transaction1.relation[0].asset.asset_id  #1

transaction2 = bbclib.make_transaction(relation_num=1, witness=True)  #2

transaction2.relations[0]\
   .set_asset_group(asset_group_1) \  #3
   .create_asset(user_id=user_1, asset_body=b'some information') \ #4
   .create_pointer(transaction_id=transaction_id_1, asset_id=asset_id_1) #4-B

transaction2.add_witness(user_1)   # 5

transaction2.add_signature(user_id=user_1, keypair=keyPair_1) #6
```

前節との違いは、#4-Bの部分だけである。BBcTransactionオブジェクトを構築する手順はどのようなトランザクションを作るときも同じであり、含めたいパーツを作り、それをaddメソッドで追加すればよい。

上記の例の#1、#2は関係するトランザクションやアセットの識別子を取得し、#4-BでそれをBBcPointerオブジェクトに格納している。なお、関係するassetが自明であれば、asset_idの方はNoneを指定しても構わない（トランザクションの中にアセットが一つしかない場合など）。



# シリアライズ/デシリアライズ

BBcTransactionオブジェクトは、そのままの形では保存や他者への送信ができないため、バイナリデータ化つまりシリアライズする必要がある。データ構造については、[BBc-1_transaction_data_ja.md](./BBc-1_transaction_data_ja.md)に解説している。下記の例は、transaction1というBBcTransactionオブジェクトをシリアライズする例である。

```python
import bbclib

txdata = bbclib.serialize(transaction1)
txdata_compressed = bbclib.serialize(transaction1, format_type=BBcFormat.FORMAT_ZLIB)
```

txdataはバイナリデータである。また、txdata_compressedはシリアライズする際にデータを圧縮したものであるが、実質的な中身（もとのBBcTrsansactionオブジェクト）は同じである。

バイナリデータを受け取ったときは、これをデシリアライズすることで、もとのBBcTransactionオブジェクトに復元することができる。

```python
import bbclib

txobj, fmt_type = bbclib.deserialize(txdata)
```

txdataがバイナリデータで、txobjがBBcTransactionオブジェクトである。ここで、bbclib.deserialize()は2つの戻り値を取ることに注意されたい。2つ目の戻り値fmt_typeは、txdataのワイヤーフォーマットの種別を示している（ワイヤーフォーマットについての[詳細はこちら](./BBc1_data_format_ja.md)）



# トランザクションの署名検証

取得したトランザクションはデシリアライズした後、改ざんが無いことを確認するために、トランザクションに付与された署名（BBcSignatureオブジェクト）の検証を行う。署名検証は、BBcSignatureオブジェクトに用意されているverify()メソッドを用いれば良い。

下記の例は、BBcSignatureオブジェクトに公開鍵が含まれている場合（version 1.4 より前）である。なお、トランザクションには3つのBBcSignatureオブジェクトが含まれているものとする。

```python
import bbclib

txobj, fmt_type = bbclib.deserialize(txdata)
digest = txobj.transaction_id

for i in range(len(txobj.signatures)):
	result = txobj.signatures[i].verify(digest)
  if not result:
    print("Verify failed...")
```

また、version 1.4からは、BBcSignatureオブジェクトに公開鍵を含めず、検証時に与えることが可能である。以下その例を示す。なお、検証に用いる公開鍵はkeyPairオブジェクトに格納されているものとする。

```python
import bbclib

txobj, fmt_type = bbclib.deserialize(txdata)
digest = txobj.transaction_id

result = txobj.signatures[0].verify(digest, pubkey=keyPair.public_key)
if not result:
  print("Verify failed...")
```



# トランザクション内の情報へのアクセス

BBcTransactionオブジェクトは先にも述べたように、他のパーツ群（BBcEvent、BBcReference、BBcRelation、BBcAsset、BBcCrossRef、BBcSignature）の器となるオブジェクトである。これらのオブジェクトが配列に格納されているので、トランザクション内の情報にアクセスするには、オブジェクト種別ごとの配列に対して要素を指定する。

例えば、BBcRelationオブジェクトを2つ含んでいて、そのそれぞれの中にさらにBBcPointerを1つずつ含んでいるとすれば、次のように情報にアクセスできる。

```python
relation_1 = txobj.relations[0]
asset_1 = relation_1.asset
asset_body_1 = asset_1.asset_body   # アセット情報が格納されているはず
pointer_1 = relation_1.pointers[0]
ptr_transactionId_1 = pointer_1.transaction_id
ptr_assetId_1 = pointer_1.asset_id

relation_2 = txobj.relations[1]
asset_2 = relation_2.asset
asset_body_2 = asset_2.asset_body   # アセット情報が格納されているはず
pointer_2 = relation_2.pointers[0]
ptr_transactionId_2 = pointer_2.transaction_id
ptr_assetId_2 = pointer_2.asset_id
```



# トランザクション作成事例

以下、BBcTransactionオブジェクトの作成事例を紹介する。なお、すべての事例についてimportや鍵ペアの生成・読み込み、asset_group_idやuser_idの設定は下記のようなコードで実施されているものとする。

```python
import bbclib

asset_group_1 = bbclib.get_new_id("asset_group_id for testing #1")
asset_group_2 = bbclib.get_new_id("asset_group_id for testing #2")

user_1 = bbclib.get_new_id("user 1")
user_2 = bbclib.get_new_id("user 2")

keyPair_user_1 = bbclib.KeyPair()
keyPair_user_1.generate()
keyPair_user_2 = bbclib.KeyPair()
keyPair_user_2.generate()
```



### BBcRelation1つ、BBcPointerなし、署名2ユーザ分

```
       +-------------------------+
       |         header          |
       +-------------------------+
       |                         |
       |        relations        |
       |     (BBcRelation x 1)   |
       |                         |
       +-------------------------+
       |                         |
       |         witness         |
       |                         |
       +-------------------------+
       |                         |
       |       signatures        |
       |    (BBcSignature x 2)   |
       |                         |
       +-------------------------+
```

```python
transaction1 = bbclib.make_transaction(relation_num=1, witness=True)

transaction1.reltions[0] \
    .set_asset_group(asset_group_1) \
    .create_asset(user_id=user_1, asset_body=b'some information')

transaction1.add_witness(user_1)
transaction1.add_witness(user_2)
transaction1.add_signature(user_id=user_1, keypair=keyPair_user_1)
transaction1.add_signature(user_id=user_2, keypair=keyPair_user_2)
```



### BBcRelation2つ、BBcPointer各2つ、署名2ユーザ分

```
       +-------------------------+
       |         header          |
       +-------------------------+
       |                         |
       |        relations        |
       |     (BBcRelation x 2)   |  <-- BBcPointer x 2 in each BBcRelation object
       |                         |
       +-------------------------+
       |                         |
       |         witness         |
       |                         |
       +-------------------------+
       |                         |
       |       signatures        |
       |    (BBcSignature x 2)   |
       |                         |
       +-------------------------+
```



下記では、transaction_id_1〜4、asset_id_1〜2が事前に生成されているものとする。

```python
transaction5 = bbclib.make_transaction(relation_num=2, witness=True)

transaction5.reltions[0] \
    .set_asset_group(asset_group_1) \
    .create_asset(user_id=user_1, asset_body=b'some information 1') \
    .create_pointer(transaction_id=transaction_id_1, asset_id=asset_id_1) \
    .create_pointer(transaction_id=transaction_id_2, asset_id=asset_id_2)

transaction5.reltions[1] \
    .set_asset_group(asset_group_2) \
    .create_asset(user_id=user_1, asset_body=b'some information 2') \
    .create_pointer(transaction_id=transaction_id_3, asset_id=None) \
    .create_pointer(transaction_id=transaction_id_4, asset_id=None)

transaction5.add_witness(user_1)
transaction5.add_witness(user_2)

transaction1.add_signature(user_id=user_1, keypair=keyPair_user_1)
transaction1.add_signature(user_id=user_2, keypair=keyPair_user_2)
```



### BBcEvent1つ (approver 1ユーザ)、BBcReferenceなし、署名1ユーザ分

```
       +-------------------------+
       |         header          |
       +-------------------------+
       |                         |
       |          events         |
       |       (BBcEvent x 1)    |
       |                         |
       +-------------------------+
       |                         |
       |         witness         |
       |                         |
       +-------------------------+
       |                         |
       |       signatures        |
       |    (BBcSignature x 1)   |
       |                         |
       +-------------------------+
```

```python
transaction6 = bbclib.make_transaction(event_num=1, witness=True)

transaction6.events[0] \
    .set_asset_group(asset_group_1) \
    .create_asset(user_id=user_1, asset_body=b'some information')

transaction6.add_witness(user_1)
transaction6.add_signature(user_id=user_1, keypair=keyPair_user_1)
```



### BBcEvent1つ (approver 1ユーザ)、BBcReference1つ、署名1ユーザ分

この例では、UTXOの入力としてBBcEventが一つ、出力としてBBcReferenceが一つのトランザクションを考える。BBcReferenceの参照先におけるBBcEventでapproverがuser_1一人だった場合を想定している。

```
       +-------------------------+
       |         header          |
       +-------------------------+
       |                         |
       |          events         |
       |       (BBcEvent x 1)    |
       |                         |
       +-------------------------+
       |                         |
       |       references        |
       |    (BBcReference x 1)   |  <-- Referring to a transaction with a single approver 
       |                         |
       +-------------------------+
       |                         |
       |       signatures        |
       |    (BBcSignature x 1)   |
       |                         |
       +-------------------------+
```



参照しているトランザクションがtransaction1で、その中の1番目のBBcEventをUTXOの入力だと想定する。

```python
transaction7 = bbclib.make_transaction(event_num=1, reference_num=1, witness=False)

transaction7.events[0] \
    .set_asset_group(asset_group_1) \
    .create_asset(user_id=user_1, asset_body=b'some information')

transaction7.create_reference(asset_group_id=asset_group_1,
                              ref_transaction_obj=transaction1,
                              event_index_in_ref=0)

transaction7.add_signature_object(user_id=user_1, keypair=keyPair_user_1)
```

