import socket
import pandas as pd
import hashlib
import time

# Load suspicious IPs from suspicious.csv
suspicious_ips = pd.read_csv('suspicious.csv')['suspicious-ip'].tolist()

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.52.11', 5004)  # Choose an appropriate IP address and port
server_socket.bind(server_address)
server_socket.listen(5)

print("Controller is waiting for incoming connections...")

while True:
    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Receive the IP address from the client
    client_ip = client_socket.recv(1024).decode()
    print(f"Received IP address from client: {client_ip}")

    # Check if the IP is in the list of suspicious IPs
    if client_ip in suspicious_ips:
        print(f"IP {client_ip} is suspicious. Sending proof of work puzzle...")

        # Generate a proof of work puzzle (simplified example)
        puzzle = hashlib.sha256(str(time.time()).encode()).hexdigest()

        # Send the puzzle to the client
        client_socket.sendall(puzzle.encode())

        # Receive the solution from the client
        solution = client_socket.recv(1024).decode()
        print(f"Received solution from client: {solution}")

        # Verify the solution (simplified example, in a real system, this would be more complex)
        if hashlib.sha256(solution.encode()).hexdigest() == puzzle:
            print("Proof of work verified. Access granted.")
        else:
            print("Proof of work verification failed. Access denied.")
    else:
        print("IP is not suspicious. Access allowed.")

    # Close the connection
    client_socket.close()
