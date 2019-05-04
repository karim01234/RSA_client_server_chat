import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import threading
import itertools
import hashlib
import time
import sys
import numpy as np

#animating loading
done = False
def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCONFIRMING CONNECTION TO SERVER '+c)
        sys.stdout.flush()
        time.sleep(0.1)



#host and port input user
host = '127.0.01'
port = int(input("Port of The Server -> "))

# printing "Server Started Message"
thread_load = threading.Thread(target=animate)
thread_load.start()

time.sleep(0.1)
done = True

length = str(input("\nLength : "))

#send, receiv funvtions
def send(t,key,length,server):
	mess = np.random.bytes(int(length))
	#encrypting the message
	cipher = PKCS1_OAEP.new(key)
	eMsg = cipher.encrypt(mess)
	if eMsg != "":
		print ("MESSAGE TO SEND TO THE SERVER-> ", str(mess))
	server.send(eMsg)


def clientThread():
	#Setting up socket
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#binding the address and port
	server.connect((host, port))
	#server's message(Public Key)
	getpbk = server.recv(2048)
	#conversion of string to KEY
	server_public_key = RSA.importKey(getpbk)
	#hashing the public key in client side for validating the hash from server
	hash_object = hashlib.sha1(getpbk)
	hex_digest = hash_object.hexdigest()
	hex_digest = hex_digest.encode('utf-8')
	
	#communication with the server
	if getpbk != "":
		server.send("YES".encode('utf-8'))
		gethash = server.recv(1024)
	if hex_digest == gethash:
		send("------Sending Message------",server_public_key,length,server)
		server.close()
	else:
		print ("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")
    	    
#threads    	
threads = []
for i in range(10):
	thread_client = threading.Thread(target=clientThread,args=())
	threads.append(thread_client)
for t in threads:
	t.start()
for t in threads:
	t.join()



    
  
