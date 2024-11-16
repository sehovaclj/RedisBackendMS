#!/bin/bash

# Constants
IMAGE_NAME="redis_backend_ms_simulation_image"
CONTAINER_NAME_PREFIX="redis_backend_ms_simulation_container_"

# Function to print messages with UTC timestamp
log() {
    echo "$(date -u +'%Y-%m-%d %H:%M:%S.%3N') $1"
}

# Stop and remove all containers matching the prefix
log "Stopping and removing containers with prefix '${CONTAINER_NAME_PREFIX}'..."
for container in $(sudo docker ps -a -q --filter "name=${CONTAINER_NAME_PREFIX}"); do
    if ! sudo docker stop "$container"; then
        log "Failed to stop container $container. Exiting..."
        exit 1
    fi
    log "Container $container stopped successfully."

    if ! sudo docker rm "$container"; then
        log "Failed to remove container $container. Exiting..."
        exit 1
    fi
    log "Container $container removed successfully."
done

# Remove the specific image
log "Removing image '${IMAGE_NAME}' (if it exists)..."
if sudo docker images -q "${IMAGE_NAME}" > /dev/null; then
    if ! sudo docker rmi -f "${IMAGE_NAME}"; then
        log "Failed to remove image ${IMAGE_NAME}. Exiting..."
        exit 1
    fi
    log "Image ${IMAGE_NAME} removed successfully."
else
    log "Image ${IMAGE_NAME} not found. Continuing..."
fi

log "All containers and images have been removed successfully."
exit 0
