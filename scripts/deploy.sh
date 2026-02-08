#!/bin/bash

echo "🚀 Deploying Camera TestGen to on-prem server..."

# Build Docker images
echo "🏗️ Building Docker images..."
docker-compose -f docker/docker-compose.yml build

# Start containers
echo "🚀 Starting containers..."
docker-compose -f docker/docker-compose.yml up -d

# Check status
echo "✅ Deployment successful!"
docker-compose -f docker/docker-compose.yml ps

echo "🌐 Access the app at: http://localhost"