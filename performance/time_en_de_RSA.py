from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import functools
import timeit
import time
import numpy as np
import matplotlib.pyplot as plt
timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

#public key and private key
random_generator = Random.new().read
RSAkey = RSA.generate(4096,random_generator)
public = RSAkey.publickey()
private = RSAkey


#encryption
def encrpt(key,whole):
	cipher = PKCS1_OAEP.new(key)
	eMsg = cipher.encrypt(whole)
	return eMsg


#decription
def dcrpt(key,newmess):
	cipher = PKCS1_OAEP.new(key)
	dMsg = cipher.decrypt(newmess)
	return dMsg
	
#storing encryption time
timesEncryp = []
timesDecryp = []
for length in range(10,128):
	mess = np.random.bytes(int(length))
	encrypt_time, res = timeit.timeit(stmt=functools.partial(encrpt, public,mess), number=20)
	timesEncryp.append(encrypt_time)
	dMsg = dcrpt(private,res)
	dcrypt_time, res = timeit.timeit(stmt=functools.partial(dcrpt, private,res), number=20)
	timesDecryp.append(dcrypt_time)


#ploting the encryption, decryption time
f, (ax1,ax2) = plt.subplots(1,2,sharex=True,sharey=True)
ax1.plot(range(10,128),timesEncryp)
ax1.set(xlabel='Message length', ylabel='Encryption time', title='Evolution of encryption time given the message length')
ax1.grid()

ax2.plot(range(10,128),timesDecryp)
ax2.set(xlabel='Message length', ylabel='Decryption time', title='Evolution of decryption time given the message length')
ax2.grid()

plt.show()
