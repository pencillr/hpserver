#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "192.168.1.27"
port = 5000                # Reserve a port for your service.
print(str(host) + ":" + str(port))
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

conn, addr = s.accept()
print 'Connected by', addr

switch = True

while switch:
#   c, addr = s.accept()     # Establish connection with client.
#   print 'Got connection from', addr
#   c.send('Thank you for connecting')
   data = conn.recv(1024) # buffer size is 1024 bytes
   data.decode("utf-8")
   print("Message: ", str(data))
   if(data == "close"):
      switch = False

print("Disconnected")
conn.close()                # Close the connection
