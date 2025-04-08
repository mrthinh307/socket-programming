# The structure of this server will include initializing sockets, listening for connections from clients, receiving HTTP requests, reading files, and sending HTTP responses with the file contents or a 404 error message if the file is not found.

# CREATE A SIMPLE WEB SERVER
# This is a simple web server that serves static HTML files over HTTP.

#import socket module
from socket import *
import sys # In order to terminate the program

# Create a socket to communicate using IPv4 and TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket (INITIALIZING SOCKETS)
serverPort = 6789 # We can change the port number here if needed
serverSocket.bind(('', serverPort)) # Bind the server socket to an address and port
serverSocket.listen(1) # LISTEN for incoming connections (1 connection at a time)

while True: 
    # Establish the connection with the client
    print('Ready to serve...') # Print a message indicating the server is ready to serve
    connectionSocket, addr = serverSocket.accept() # Accept the client connection
    try:
        # RECEIVE the HTTP request from the client
        massage = connectionSocket.recv(1024).decode() # Buffer size of 1024 bytes
        
        # Extract the requested file name from the HTTP request
        filename = massage.split()[1] # Get the requested file name from the HTTP GET request
        print(f"Client requested: {filename}")

        # Open the requested file
        with open(filename[1:], 'r') as f:
            outputdata = f.readlines() # Read all lines from the file
            
        # Lấy tên file từ HTTP request, ví dụ: "GET /HelloWorld.html HTTP/1.1"
        # filename = message.split()[1]  # filename = "/HelloWorld.html"
        # f = open(filename[1:])         # Bỏ dấu "/" để mở file "HelloWorld.html"
        # outputdata = f.read()         # Đọc nội dung file
        
        # Send HTTP header line into socket
        # If the file is found, send a 200 OK response
        header = 'HTTP/1.1 200 OK\r\n'
        header += 'Content-Type: text/html\r\n\r\n'
        connectionSocket.send(header.encode())
        
        # Send the content of the requested file to the client
        for line in outputdata:
            connectionSocket.send(line.encode()) # Send each line of the file
            
        connectionSocket.close()  # Close the connection to the client
    except IOError:
        # If the file is not found, send a 404 Not Found response
        error_message = 'HTTP/1.1 404 Not Found\r\n'
        error_message += 'Content-Type: text/html\r\n\r\n'
        error_message += '<html><body><h1>404 Not Found</h1></body></html>'

        connectionSocket.send(error_message.encode())  # Send error message

        #Close client socket
        connectionSocket.close()  # Close the connection
    
# Close the server socket
serverSocket.close()
sys.exit()  # Terminate the program
