import socket

serverName = '192.168.1.79' 
serverPort = 12000 

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort)) 

isContinue = True

while isContinue:
    message = input('Enter a message: ')

    clientSocket.send(message.encode())

    if message == 'quit':
        isContinue = False
        break

    recevMessage = clientSocket.recv(1024) 
    print ('From Server:', recevMessage.decode())  
clientSocket.close()