import os
import subprocess
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import socket
import hashlib
import time

# Load the pre-trained model
model_path = '/path/to/birch.h5'
model = tf.keras.models.load_model(model_path)

# Define the features used for classification
features_14 = [
    'Bwd IAT Min', 'Bwd IAT Mean', 'Src Port', 'Protocol', 'Bwd IAT Tot', 'Flow IAT Max', 'Dst Port', 
    'Bwd Header Len', 'Flow IAT Min', 'Flow Pkts/s', 'Bwd IAT Max', 'Flow Duration', 'Bwd Pkts/s', 'Flow IAT Std'
]

def capture_packets(interface):
    """Capture packets from the specified network interface using tcpdump."""
    output_file = '/opt/scripts/captured_packets.pcap'
    command = ['tcpdump', '-i', interface, '-w', output_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def convert_packets_to_features(pcap_file):
    """Convert captured packets to features using CICFlowMeter."""
    cicflowmeter_jar = '/path/to/cfm.jar'
    command = ['java', '-jar', cicflowmeter_jar, '-i', pcap_file, '-o', '/opt/scripts/']
    subprocess.run(command, check=True)
    csv_file = os.path.join('/opt/scripts/', 'flows.csv')
    return csv_file

def classify_packets(csv_file):
    """Classify packets as normal or attacker using the pre-trained model."""
    df = pd.read_csv(csv_file)
    X = df[features_14].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    predictions = model.predict(X_scaled)
    return np.mean(predictions) > 0.5

def grant_access():
    """Grant access to the instance."""
    print("Access granted.")

def deny_access_and_send_puzzle():
    """Deny access and send a proof-of-work puzzle."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 12345))
    sock.listen(1)
    print("Waiting for instance to connect...")
    conn, addr = sock.accept()
    print(f"Connection from {addr}")
    puzzle = hashlib.sha256(b'some_random_puzzle').hexdigest()
    conn.sendall(puzzle.encode())
    received_puzzle = conn.recv(1024).decode()
    if received_puzzle == hashlib.sha256(b'some_random_solution').hexdigest():
        print("Puzzle solved. Access granted.")
    else:
        print("Puzzle not solved. Access denied.")
    conn.close()

def main():
    while True:
        # Start packet capture
        process = capture_packets('br-int')
        
        # Wait for some time  before stopping packet capture
        time.sleep(1)
        process.terminate()
        
        # Convert captured packets to features using CICFlowMeter
        csv_file = convert_packets_to_features('/opt/scripts/captured_packets.pcap')
        
        # Classify packets
        if classify_packets(csv_file):
            grant_access()
        else:
            deny_access_and_send_puzzle()

if __name__ == "__main__":
    main()
