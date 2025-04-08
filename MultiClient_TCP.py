import socket
import threading

def receive_messages(client_socket):
    """Function to continuously receive messages from the server"""
    try:
        while True:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                # If no data is received, server has disconnected
                print("Server has disconnected")
                break
            
            # Display the received message
            print(f"\nFrom Server: {data.decode()}")

    except Exception as e:
        # Handle any exceptions that occur during receiving
        print(f"Error receiving message: {e}")

def main():
    # Define server address and port
    server_name = '192.168.1.79'  # Server address
    server_port = 12000        # Server port
    
    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((server_name, server_port))
        print(f"Connected to server {server_name}:{server_port}")
        
        # Create and start a thread for receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True  # Thread will terminate when the main program ends
        receive_thread.start()
        
        print("Type 'exit' to quit")
        
        # Loop for sending messages
        while True:
            message = input("Enter message: ")
            
            if message.lower() == 'exit':
                # Exit the loop if user types 'exit'
                break
                
            # Send the message to the server
            client_socket.send(message.encode())
            
    except Exception as e:
        # Handle any exceptions that occur during connection or sending
        print(f"Error: {e}")
    finally:
        # Always close the connection when exiting
        client_socket.close()
        print("Disconnected")

if __name__ == "__main__":
    main()