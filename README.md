# blockchain demos

This just contains some code that I wrote to see if I'm understanding the
blockchain protocol documentation correctly. In case somehow you stumbled
on this repository looking for information on the format of the blockchain,
let me point you to:

https://en.bitcoin.it/wiki/Protocol_documentation

That's what I'm looking at :-)

## Notes

To obtain a raw transaction use blockexplorer's <code>/api/rawtx/</code>
link followed by the transaction id. For example: 

https://blockexplorer.com/api/rawtx/7c402505be883276b833d57168a048cfdf306a926484c0b58930f53d89d036f9

gets the example transaction of .319 BTC from Michael Nielsen's post:

http://www.michaelnielsen.org/ddi/how-the-bitcoin-protocol-actually-works/

What you get back (in this particular case) is:<pre>
{"rawtx":"01000000013e0ca0834b01977c0a066dd1b2942e416c9273e876a46ad3dcb1a128c7ae0720000000008b48304502205014856cdf89da70ad9a4f223bac4e5477da5c6cb69ef2b9f8b5f8548e21307e0221009bfe2698f1eb1c561f41981d8e78c11d9e685a70e682f144ee6c8ab5ecb0497c0141042b2d8def903dd62d0c4161ed8d4ccfa5967e11a28e65cb141235b7c27d8ef6aa3bd63be077323cf3d7e0e8895b264b94feb4b40478b431da6f45dfc8e1004f62ffffffff0160c1e601000000001976a914a7db6ff121871c65a8924b8e40f160d385515ad788ac00000000"}</pre>

Looks to me like this is JSON and the actual transaction is:

<pre>01000000013e0ca0834b01977c0a066dd1b2942e416c9273e876a46ad3dcb1a128c7ae0720000000008b48304502205014856cdf89da70ad9a4f223bac4e5477da5c6cb69ef2b9f8b5f8548e21307e0221009bfe2698f1eb1c561f41981d8e78c11d9e685a70e682f144ee6c8ab5ecb0497c0141042b2d8def903dd62d0c4161ed8d4ccfa5967e11a28e65cb141235b7c27d8ef6aa3bd63be077323cf3d7e0e8895b264b94feb4b40478b431da6f45dfc8e1004f62ffffffff0160c1e601000000001976a914a7db6ff121871c65a8924b8e40f160d385515ad788ac00000000</pre>
