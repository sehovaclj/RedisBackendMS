#!/bin/bash

# Constants
IMAGE_NAME="redis_backend_ms_simulation_image"
CONTAINER_NAME_PREFIX="redis_backend_ms_simulation_container_"

# Function to print messages with UTC timestamp
log() {
    echo "$(date -u +'%Y-%m-%d %H:%M:%S.%3N') $1"
}

# Run pylint for linting checks
log "Running pylint..."
if ! pylint . ; then
    log "Pylint failed. Exiting..."
    exit 1
fi
log "Pylint completed successfully."

# Run unit tests
log "Running unit tests..."
if ! pytest -v ; then
    log "Unit tests failed. Exiting..."
    exit 1
fi

# Remove existing containers if any
log "Removing existing containers..."
for container in $(sudo docker ps -a -q --filter "name=${CONTAINER_NAME_PREFIX}"); do
    if ! sudo docker rm -f "$container" ; then
        log "Failed to remove container $container. Exiting..."
        exit 1
    fi
    log "Container $container removed successfully."
done

# Remove the image if it exists
log "Removing existing image (if any)..."
if sudo docker images -q "${IMAGE_NAME}" ; then
    if ! sudo docker rmi -f "${IMAGE_NAME}" ; then
        log "Failed to remove image ${IMAGE_NAME}. Exiting..."
        exit 1
    fi
    log "Image ${IMAGE_NAME} removed successfully."
else
    log "No image ${IMAGE_NAME} found. Continuing..."
fi

# Build the docker image with no cache
log "Building the Docker image with no cache..."
if ! sudo docker build --no-cache -t "${IMAGE_NAME}" . ; then
    log "Docker build failed. Exiting..."
    exit 1
fi
log "Docker image built successfully."

# Get the number of containers to run from the argument passed
NUM_CONTAINERS=$1
if [[ -z "$NUM_CONTAINERS" || ! "$NUM_CONTAINERS" =~ ^[0-9]+$ ]]; then
    log "Invalid number of containers specified. Exiting..."
    exit 1
fi

# Run the specified number of containers
log "Starting $NUM_CONTAINERS containers..."
for i in $(seq 1 "$NUM_CONTAINERS"); do
    container_name="${CONTAINER_NAME_PREFIX}${i}"
    if ! sudo docker run -d --name "$container_name" --network="host" "${IMAGE_NAME}" ; then
        log "Failed to start container $container_name. Exiting..."
        exit 1
    fi
    log "Container $container_name started successfully."
done

log "All steps completed successfully."
exit 0
