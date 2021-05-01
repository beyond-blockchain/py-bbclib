py-bbclib
====

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CircleCI](https://circleci.com/gh/beyond-blockchain/py-bbclib.svg?style=shield)](https://circleci.com/gh/beyond-blockchain/py-bbclib)


The library that defines BBc-1 transaction data structure is decoupled from [the bbc1 repository](https://github.com/beyond-blockchain/bbc1).

BBc-1 is a Python-based reference implementation of BBc-1, a trustable system of record keeping beyond blockchains. The transaction data structure definition is the most important part of BBc-1.
      
The design paper (white paper) and the analysis paper are available [here](https://beyond-blockchain.org/public/bbc1-design-paper.pdf) and [here](https://beyond-blockchain.org/public/bbc1-analysis.pdf). BBc-1 is inspired from blockchain technologies like Bitcoin, Ethereum, Hyperledger projects, and so on.
BBc-1 is a simple but reliable distributed ledger system in contrast with huge and complicated existing blockchain platforms.
The heart of BBc-1 is the transaction data structure and the relationship among transactions, which forms a graph topology.
A transaction should be signed by the players who are the stake holders of the deal. BBc-1 achieves data integrity and data transparency by the topology of transaction relationship and signatures on transactions. Simply put, BBc-1 does not have *blocks*, and therefore, requires neither mining nor native cryptocurrency.
BBc-1 can be applied to both private/enterprise use and public use. BBc-1 has a concept of *domain* for determining a region of data management. Any networking implementation (like Kademlia for P2P topology management) can be applied for each domain.
Although there are many TODOs in BBc-1, this reference implementation includes most of the concept of BBc-1 and would work in private/enterprise systems. When sophisticated P2P algorithms are ready, BBc-1 will be able to support public use cases.

For the details, please read documents in [docs/ directory](https://github.com/beyond-blockchain/py-bbclib/tree/develop/docs) or [the bbc1 repository](https://github.com/beyond-blockchain/bbc1). Not only documents but slide decks (PDF) explain the design of the BBc-1 and its implementation.

API doc is ready at [readthedocs.org](https://py-bbclib.readthedocs.io/en/latest/index.html).

## libbbcsig becomes optional at v1.5.3

Before v1.5.2, [libbbcsig module](https://github.com/beyond-blockchain/libbbcsig) was required by py-bbclib. So, building libbbcsig at pip install took very long time, and sometimes it leads to cache problem. py-bbclib v1.5.3 newly includes [cryptograpy module](https://github.com/pyca/cryptography) for crypto-related procedures. KeyPairPy class in bbclib_keypair.py includes the new feature and KeyPairFast class in bbclib_keypair_fast.py is the same script as bbclib_keypair.py in the older version. bbclib_keypair.py automatically checks whether libbbcsig is installed or not, and if not installed, bbclib_keypair.py fallbacks to use cryptography module based class.

Just run,

```bash
    pip install py-bbclib
```

You will find that the module is installed more quickly than before.

The drawback of using fallback mode ([cryptograpy module](https://github.com/pyca/cryptography)) is slower transaction speed. Concretely, sign/verify speed is about half as fast as that of libbbcsig based mode.

The sign/verify performance comparison on MacBookPro 2016 (2.7 GHz Quad core Intel Core i7 with 16GB RAM) is shown below.

| Mode                   | time to complete 20,000 times sign and verify |
| ---------------------- | --------------------------------------------- |
| use libbbcsig          | about 8 seconds                               |
| use cryptograpy module | about 15 seconds                              |
| bbclib-go              | about 4 seconds                              |

*condition: The test code creates a BBcTransaction object with 2 signatures and verify this transaction object. This unit of sign/verify process is iterated 10,000 times.*



## Namespace is changed at v1.4.1 

Before v1.4.1, the namesapce of py-bbclib module was "bbc1". However, This conflicts with that of bbc1 module.
Therefore, the namespace of py-bbclib has been changed to "bbclib" since v1.4.1.
Be careful when using py-bbclib module solely.


## Environment

* Python
    - Python 3.5.0 or later
    - virtualenv is recommended
        - ```python -mvenv venv```

* tools for macOS by Homebrew
    ```
    xcode-select --install
    brew install libtool automake python3 openssl
    pip3 install virtualenv
    ```
    
* tools for Linux (Ubuntu 16.04 LTS, 18.04 LTS)
    ```
    sudo apt-get update
    sudo apt-get install -y git tzdata openssh-server python3 python3-dev python3-pip python3-venv libffi-dev net-tools autoconf automake libtool libssl-dev make
    ```

## Install

```bash
    python -mvenv venv
    source venv/bin/activate
    pip install py-bbclib
```

### install libbbcsig (optional)
An external library, [libbbcsig](https://github.com/beyond-blockchain/libbbcsig) makes sign/verify of transaction data faster. After pip install, two utilities are installed in your venv/bin. 

"install_libbbcsig" command downloads the libbbcsig repository, builds libbbcsig and installs the dynamic link library in your venv. Just run as follows:

```bash
    install_libbbcsig
```

install_libbbcsig command builds the library in /tmp/tmp.libbbcsig.xxxxx directory (xxxxx part is the process number). If you want to reuse the module, you can use "copy_libbbcsig" command to copy library from the repository directory that includes the built library as follows:

```
    copy_libbbcsig /tmp/tmp.libbbcsig.xxxxx
```

