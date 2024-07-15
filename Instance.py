import socket
import hashlib
import time

# Replace 'controller_ip' and 'controller_port' with the actual IP address and port of the controller
controller_ip = '192.168.52.11'
controller_port = 5004

# Create a socket to connect to the controller
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller_address = (controller_ip, controller_port)

try:
    # Connect to the controller
    client_socket.connect(controller_address)
    print(f"Connected to controller at {controller_address}")

    # Get the local IP address (you might need to adjust this based on your network setup)
    local_ip = socket.gethostbyname(socket.gethostname())

    # Send the local IP address to the controller
    client_socket.sendall(local_ip.encode())
    print(f"Sent local IP address to controller: {local_ip}")

    # Receive the proof of work puzzle from the controller
    puzzle = client_socket.recv(1024).decode()
    print(f"Received proof of work puzzle: {puzzle}")

    # Solve the proof of work puzzle (simplified example)
    solution = hashlib.sha256(str(time.time()).encode()).hexdigest()

    # Send the solution to the controller
    client_socket.sendall(solution.encode())
    print(f"Sent solution to controller: {solution}")

finally:
    # Close the connection
    client_socket.close()
