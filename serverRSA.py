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
host= str(input("Server Address - > "))
port = int(input("Port - > "))

#boolean for checking server and port
check = False
done = False


def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCHECKING IP ADDRESS AND NOT USED PORT '+c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r-----SERVER STARTED. WAITING FOR CLIENT-----\n')
    
#public key and private key
random_generator = Random.new().read
RSAkey = RSA.generate(1024,random_generator)
public = RSAkey.publickey().exportKey()
private = RSAkey.exportKey()

#hashing the public key
hash_object = hashlib.sha1(public)
hex_digest = hash_object.hexdigest()


try:
    #setting up socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
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
#time.sleep(0.5)
done = True

#binding client and address
client,address = server.accept()
print ("CLIENT IS CONNECTED. CLIENT'S ADDRESS ->",address)
print ("-----WAITING FOR PUBLIC KEY & PUBLIC KEY HASH-----")

#communicating

while True:
	#sending public key
    client.send(public)
    #getting confirmation from client of key receiving
    confirm = client.recv(1024).decode('utf-8')
    if confirm == "YES":
    	#sending HEX_DIGEST for validation
        client.send(hex_digest.encode('utf-8'))
        
    print ("-----HANDSHAKE COMPLETE-----")
    while True:
        #message from client
        newmess = client.recv(1024)
        #encryption
        cipher = PKCS1_OAEP.new(RSAkey)
        dMsg = cipher.decrypt(newmess)
        print ("\n**New Message**  "+time.ctime(time.time()) +" > "+dMsg.decode('utf-8')+"\n")
    client.close()        	
	
    
    
    
	
