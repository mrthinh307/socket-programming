import socket
import threading


# Define a class ClientThread that handles communication with a single client
class ClientThread(threading.Thread):
    def __init__(self, conn_socket, client_addr):
        # Call the constructor of the parent class (Thread)
        threading.Thread.__init__(self)
        # Save the client's connection socket and address
        self.conn_socket = conn_socket
        self.client_addr = client_addr
        # A flag to control the thread loops
        self.running = True

        # Print a message when a new client connects
        print(f"New connection from: {client_addr[0]}:{client_addr[1]}")

    # Function to receive messages from the client
    def receive_from_client(self):
        try:
            while self.running:
                # Wait to receive data from the client (max 1024 bytes)
                data = self.conn_socket.recv(1024)
                if not data:
                    # If no data is received, the client disconnected
                    print(f"Client {self.client_addr[0]}:{self.client_addr[1]} has disconnected")
                    self.running = False
                    break

                # Decode bytes to string and print the client's message
                message = data.decode()
                print(f"[Client {self.client_addr[0]}:{self.client_addr[1]}] says: {message}")
        except Exception as e:
            # Handle any exception during communication
            print(f"Error with client {self.client_addr[0]}:{self.client_addr[1]}: {e}")
        finally:
            # Always close the connection when done
            self.conn_socket.close()

    # Function to send messages from the server keyboard to the client
    def send_to_client(self):
        try:
            while self.running:
                # Read a message from the server operator (keyboard input)
                message = input(f"[Server -> {self.client_addr[0]}:{self.client_addr[1]}] Enter message: ")

                # If the message is 'exit', close the connection
                if message.lower() == "exit":
                    self.running = False
                    self.conn_socket.close()
                    break

                # Send the typed message to the client
                self.conn_socket.send(message.encode())
        except:
            # Ignore errors if any occur (e.g., broken pipe)
            pass

    # This method is called when the thread starts
    def run(self):
        # Create a new thread to receive messages from the client
        recv_thread = threading.Thread(target=self.receive_from_client)
        # Create another thread to send messages to the client
        send_thread = threading.Thread(target=self.send_to_client)
        
        # Start both threads
        recv_thread.start()
        send_thread.start()

        # Wait until both threads finish
        recv_thread.join()
        send_thread.join()


def main():
    # Define server port and create the socket
    server_port = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket option to allow reuse of address and port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to all interfaces on the specified port
    server_socket.bind(('', server_port))
    # Listen for connections, queue up to 5 connection requests
    server_socket.listen(5)
    
    print(f"Server is listening on port {server_port}")
    
    try:
        while True:
            # Accept a new connection
            connection_socket, client_addr = server_socket.accept()
            
            # Create and start a new thread for each client
            new_thread = ClientThread(connection_socket, client_addr)
            new_thread.start()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Server is shutting down...")
    finally:
        # Always close the server socket when exiting
        server_socket.close()

if __name__ == "__main__":
    main()