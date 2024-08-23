# ddos-detection
A model to detect DDoS attacks in sdn environment using unsupervised learning and puzzle based mechanism

# Setting Up a Python Daemon Process on OpenStack Neutron Node

This guide will walk you through the process of setting up a Python script as a daemon process on the Neutron node of an OpenStack Yoga environment. The daemon process will continuously run a `capture.py` script that logs timestamps to a file at regular intervals.

## Prerequisites

- OpenStack Yoga environment with Neutron node
- Basic knowledge of `systemd` and Linux command-line
- Python 3 installed on the Neutron node

## Step 1: Create the Python Script

First, create a Python script (`capture.py`) that logs the current timestamp to a log file every 10 seconds.

### **Script: `capture.py`**

## Step 2: Create the script
sudo mkdir -p /opt/scripts
sudo nano /opt/scripts/capture.py

## Step 3: Make the script executable

sudo chmod +x /opt/scripts/capture.py

## Step 4: create Systemd service file

### Create the Service File:
sudo nano /etc/systemd/system/capture.service

### Reload the Systemd Daemon:
sudo systemctl daemon-reload

### Enable the Service to Start on Boot:
sudo systemctl enable capture.service

### Start the Service Manually:
sudo systemctl start capture.service

