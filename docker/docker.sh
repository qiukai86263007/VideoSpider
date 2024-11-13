#!/bin/bash

# Define the log file
LOG_FILE="./docker_script.log"

# Function to build Docker images
build() {
    echo "Building Docker images..." | tee -a "$LOG_FILE"
    docker-compose build 2>&1 | tee -a "$LOG_FILE"
    echo "Docker images built successfully." | tee -a "$LOG_FILE"
}

# Function to start Docker containers
up() {
    echo "Starting Docker containers..." | tee -a "$LOG_FILE"
    docker-compose up -d 2>&1 | tee -a "$LOG_FILE"
    echo "Docker containers started successfully." | tee -a "$LOG_FILE"
}

# Function to stop and remove Docker containers, networks, and volumes
down() {
    echo "Stopping and removing Docker containers, networks, and volumes..." | tee -a "$LOG_FILE"
    docker-compose down -v 2>&1 | tee -a "$LOG_FILE"
    echo "Docker containers, networks, and volumes removed successfully." | tee -a "$LOG_FILE"
}

# Check the command-line argument
case "$1" in
    build)
        build
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    *)
        echo "Usage: $0 {build|up|down}" | tee -a "$LOG_FILE"
        exit 1
        ;;
esac