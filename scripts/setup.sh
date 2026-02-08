#!/bin/bash

echo "🚀 Setting up Camera TestGen..."

# Create required directories
mkdir -p data/input_screenshots
mkdir -p data/kb
mkdir -p data/exports
mkdir -p data/logs

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd src/frontend
npm install
cd ../..

echo "✅ Setup completed!"