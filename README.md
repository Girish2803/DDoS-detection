# DDoS Detection System for SDN Environments
## Overview
This project aims to detect Distributed Denial of Service (DDoS) attacks in a Software-Defined Networking (SDN) environment using unsupervised learning and a proof-of-work mechanism. The system is designed to monitor network traffic, classify it, and take appropriate actions based on the classification results.

## System Flow
### 1. Neutron Script Always Running
A Python script, capture.py, is set up as a daemon process on the Neutron node. This script continuously logs timestamps to a file at regular intervals and captures network traffic.
File Path: /opt/scripts/capture.py 

### 2. Packet Capture and Classification
When an instance attempts to ping the controller, packets are generated and captured by the Neutron node. The captured packets are then analyzed to determine if the host is normal or suspicious.

Packet Capture: Handled by the capture_packets() function in the Neutron node script.
Feature Extraction: Packets are converted to features using the convert_packets_to_features() function, which utilizes the CICFlowMeter tool.
Classification: The classify_packets() function applies a pre-trained model (BIRCH clustering) to classify the host based on the extracted features.
If the host is classified as normal, access is granted directly.

### 3. Proof-of-Work Mechanism for Suspicious Hosts
If the host is detected as suspicious, a socket-based communication is established between the Neutron node and the instance. The Neutron node sends a proof-of-work SHA256 puzzle to the instance.

Puzzle Generation: Done using the deny_access_and_send_puzzle() function in the Neutron node script.
Solution Validation: The instance must solve the puzzle correctly to gain access. The solution is verified by the Neutron node.
If the instance provides the correct solution, access is granted; otherwise, access is blocked.

## Implementation
Neutron Node Script
File Path: /opt/scripts/neutron_script.py
Functionality: Captures packets, extracts features, classifies the host, and handles the proof-of-work mechanism.
Instance Script
Normal Host Script: normal_host.py
Attacker Host Script: attacker_host.py
Functionality: Simulates network traffic and interacts with the Neutron node for puzzle solving.
Setup Instructions
Setting Up the Python Daemon Process on Neutron Node
Create the Python Script:

Run sudo mkdir -p /opt/scripts
Run sudo nano /opt/scripts/capture.py and add the capture.py script content.
Make the Script Executable:

Run sudo chmod +x /opt/scripts/capture.py
Create the Systemd Service File:

Run sudo nano /etc/systemd/system/capture.service and add the service configuration.
Reload the Systemd Daemon:

Run sudo systemctl daemon-reload
Enable the Service to Start on Boot:

Run sudo systemctl enable capture.service
Start the Service Manually:

Run sudo systemctl start capture.service
References
CICFlowMeter GitHub Repository
Pre-trained BIRCH Model
