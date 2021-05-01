Change log
======

## v1.6.1
* update modules
* fix import problem regarding collections

## v1.6
* support method-chain style coding to create transaction object

## v1.5.6
* modify dynamic link library load procedure for AWS lambda

## v1.5.5
* bug fix on reading PEM key file

## v1.5.4  (invalidated and removed from PyPI)
* bug fix

## v1.5.3
* implement python cryptography module based KeyPair class (KeyPairPy)
* py-bbclib module works without libbbcsig library (fallback mode)
  - building libbbcsig becomes optional, so pip installation speed becomes quite faster.

## v1.5.2

* add assertion in BBcRelation and BBcEvent

## v1.5.1
* bug fix

## v1.5
* add BBcAssetRaw and BBcAssetHash classes
* the version in BBcTransaction header is ~~3~~ 2

## v1.4.4
* Bug fix

## v1.4.3
* modify key import function to use libbcsig v1.4 for setting curvetype in KeyPair object

## v1.4.2
* modify transaction validation tool for bbc1 (skip signature validation if no public key included)

## v1.4.1
* change namespace of module from "bbc1" to "bbclib"

## v1.4
* ID length configuration support
* External public key support
  * BBcSignature having 0-length public key indicates that the public key for verification is given externally.

## v1.3
* Decoupled from bbc1 repository
  * Complete the same functions as those of the original bbc1 version 1.3
