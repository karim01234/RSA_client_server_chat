import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import threading
import itertools
import hashlib
import time
import sys


#animating loading
done = False
def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCONFIRMING CONNECTION TO SERVER '+c)
        sys.stdout.flush()
        time.sleep(0.1)

#Setting up socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#host and port input user
host= str(input("Server Address - > "))
port = int(input("Port of The Server -> "))

#binding the address and port
server.connect((host, port))

# printing "Server Started Message"
thread_load = threading.Thread(target=animate)
thread_load.start()

#time.sleep(0.5)
done = True

#server's message(Public Key)
getpbk = server.recv(2048)

#conversion of string to KEY
server_public_key = RSA.importKey(getpbk)

#hashing the public key in client side for validating the hash from server
hash_object = hashlib.sha1(getpbk)
hex_digest = hash_object.hexdigest()
hex_digest = hex_digest.encode('utf-8')


#send, receiv funvtions
def send(t,name,key):
	mess = str(input(name + " : "))
	    #merging the message and the name
	whole = name+" : "+mess
	whole = whole.encode('utf-8')
	    #encrypting the message
	cipher = PKCS1_OAEP.new(key)
	eMsg = cipher.encrypt(whole)
	server.send(eMsg)

def recv(t,key):
	key = RSA.importKey(key)
	newmess = server.recv(1024)
	newmess = newmess.decode('utf-8')
	
	'''
    print ("\nENCRYPTED MESSAGE FROM SERVER-> " + newmess)
    cipher = PKCS1_OAEP.new(key)
    dMsg = cipher.decrypt(newmess)
    '''
	print ("\n**New Message From Server**  " + time.ctime(time.time()) + " : " + newmess + "\n")



#communication with the server

if getpbk != "":
    server.send("YES".encode('utf-8'))
    gethash = server.recv(1024)
if hex_digest == gethash:
    print ("\n-----HANDSHAKE COMPLETE-----")
    alais = str(input("\nYour Name -> "))
    while True:
    	send("------Sending Message------",alais,server_public_key)
    	time.sleep(6)
    server.close()          	
else:
    print ("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")
    
  
