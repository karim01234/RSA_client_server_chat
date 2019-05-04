# RSA_client_server_chat
This project presents an RSA encryption of the communication between a client and aserver
### How it works
The server:
  - generates the private and public key
  - wait for connection
  - send the public key for the client if he connects

The client
  - encrypt the message and send it to the server using the public key

The server
  - decrypt the message using the private key
      
### Run
to run the server:

    python3 serverRSA.py
to run the client:

    python3 clientRSA.py
### Requires
Python libraries:
  - socket
  - pycrypto
### Multiparaller version
In this part, i used the python threads in order to enable the server to communicate with many clients, for this purpose, i 
modelized many clients in "clientRsaPara.py" , each of them send a message with a length that we choose. For the server part, in 
"serverRsaPara.py" , each thread represents a  connection.

### RSA performance function of message length
in "time_en_de_RSA.py", i drew the variation of the encryption and decryption time function of the message length variating from 10 to 128 bytes, as a result, the diration is approximately constant
