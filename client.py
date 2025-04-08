import socket
import sys

def main():
    # Check command line arguments
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)
    
    # Get command line arguments
    server_host = sys.argv[1] # Hostname or IP address of the server
    server_port = int(sys.argv[2]) # Port number of the server
    filename = sys.argv[3] # Name of the file to request from the server
    
    try:
        # Create TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        print(f"Connecting to {server_host}:{server_port}...")
        client_socket.connect((server_host, server_port))
        
        # Construct HTTP request
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        
        # Send HTTP request
        print(f"Sending request for /{filename}")
        client_socket.send(request.encode())
        
        # Receive the response
        print("Waiting for response...")
        
        # Initialize variables for receiving data
        response = b""
        buffer_size = 4096
        
        # Keep receiving data until there's no more
        while True:
            data = client_socket.recv(buffer_size)
            if not data:
                break
            response += data
        
        # Close the socket
        client_socket.close()
        
        # Split response into headers and body
        response_str = response.decode('utf-8', errors='replace')
        header_end = response_str.find('\r\n\r\n')
        
        if header_end != -1:
            headers = response_str[:header_end]
            body = response_str[header_end + 4:]  # +4 to skip \r\n\r\n
            
            # Print the response
            print("\n===== HTTP Response Headers =====")
            print(headers)
            print("\n===== HTTP Response Body =====")
            print(body)
        else:
            # If can't split properly, just print everything
            print("\n===== HTTP Response =====")
            print(response_str)
        
    except Exception as e:
        print(f"Error: {e}")
        if 'client_socket' in locals():
            client_socket.close()
        sys.exit(1)

if __name__ == "__main__":
    main()