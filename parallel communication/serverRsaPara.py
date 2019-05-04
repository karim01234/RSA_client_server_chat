import socket
import hashlib
import os
import time
import itertools
import threading
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

#server address and port number input from admin
host = ''
port = int(input("Port - > "))

#boolean for checking server and port
check = False
done = False

#animation for checking adress
def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCHECKING IP ADDRESS AND NOT USED PORT '+c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r -----SERVER STARTED. WAITING FOR CLIENT-----\n')
    
#generating public key and private key
random_generator = Random.new().read
RSAkey = RSA.generate(2048,random_generator)
public = RSAkey.publickey().exportKey()
private = RSAkey.exportKey()

#hashing the public key
hash_object = hashlib.sha1(public)
hex_digest = hash_object.hexdigest()

#server socket
try:
    #setting up socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    check = True
except BaseException:
    print("-----Check Server Address or Port-----")
    check = False

if check is True:
    # server Quit
    shutdown = False
# printing "Server Started Message"
thread_load = threading.Thread(target=animate)
thread_load.start()
time.sleep(0.1)
done = True


#communicate function
def communicate(client,adress):
	client.send(public)
	confirm = client.recv(1024).decode('utf-8')
	if confirm == "YES":
		#sending HEX_DIGEST
		client.send(hex_digest.encode('utf-8'))
	#message from client
	newmess = client.recv(1024)
	cipher = PKCS1_OAEP.new(RSAkey)
	dMsg = cipher.decrypt(newmess)
	print ("**New Message**  "+time.ctime(time.time()) +" > "+str(dMsg))
	client.close() 
    
while True:
	#listening
	server.listen(1)
	#binding client and address
	client,address = server.accept()
	print ("CLIENT IS CONNECTED. CLIENT'S ADDRESS ->",address)
	thread = threading.Thread(target=communicate,args=(client,address))
	thread.start()




       	
	
    
    
    
	
