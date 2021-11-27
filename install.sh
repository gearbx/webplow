#!/bin/bash
echo "Install Python dependencies..."
pip install -r requirements.txt
echo "Copying script to /usr/local/bin..."
sudo cp ./webplow.py /usr/local/bin
