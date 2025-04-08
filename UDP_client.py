import socket

serverName = '10.11.53.63' 
serverPort = 12000 

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
clientSocket.connect((serverName,serverPort)) 

isContinue = True

while isContinue:
    sentence = input('Enter message: ') 

    clientSocket.send(sentence.encode()) 

    if sentence == 'quit':
        isContinue = False
        break

    recevMessage = clientSocket.recv(1024) 
    print ('From Server:', recevMessage.decode())  
clientSocket.close()