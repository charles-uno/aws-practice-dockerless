#!/bin/bash

IMAGE_TAG=django-amulet-image
CONTAINER_PORT=8000
HOST_PORT=8001
ROOT_DIR=$(realpath $0 | xargs dirname | xargs dirname)

# Container is launched in the background by default. Debug means launch it in
# the foreground so we can see the output
DEBUG=true
FORCE=false
for ARG in $@; do
    if [[ "$ARG" == "-d" || "$ARG" == "--debug" ]]; then
        DEBUG=true
    fi
    if [[ "$ARG" == "-f" || "$ARG" == "--force" ]]; then
        FORCE=true
    fi
done

CONFLICTING_CONTAINER=$(docker ps | grep "0.0.0.0:$HOST_PORT->" | awk '{print $1}')
if [[ "$CONFLICTING_CONTAINER" != "" ]]; then
    if [[ "$FORCE" == "true" ]]; then
        echo "killing conflicting container $CONFLICTING_CONTAINER"
        docker stop "$CONFLICTING_CONTAINER"
    else
        echo "encountered conflict $CONFLICTING_CONTAINER, use --force to override"
        exit 1
    fi
fi

docker build -f "$ROOT_DIR/app/Dockerfile" -t "$IMAGE_TAG" "$ROOT_DIR"

if [[ "$DEBUG" == "true" ]]; then
    docker run --name "$CONTAINER_NAME" -p "$HOST_PORT:$CONTAINER_PORT" "$IMAGE_TAG"
else
    docker run -d --name "$CONTAINER_NAME" -p "$HOST_PORT:$CONTAINER_PORT" "$IMAGE_TAG"
fi


