import socket

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('The server is ready to receive')
    connectionSocket, addr = serverSocket.accept() # Blocking call, waiting for a client to connect
    print('Connect with:', addr)
    isContinue = True
    while isContinue:
        sentence = connectionSocket.recv(1024).decode()
        print('Client:', addr, 'sent:', sentence)
        if sentence == 'quit':
            isContinue = False
            break
        replyMessage = input("Server: ")
        connectionSocket.send(replyMessage.encode()) 

    connectionSocket.close() 
    print('Close connect with:', addr)

