#!/bin/bash

if [[ "$(uname)" == "Darwin" ]]; then
  # macOS
  if [[ "$(uname -m)" == "arm64" ]]; then
    PLATFORM="linux/arm64"
  else
    PLATFORM="linux/amd64"
  fi
elif [[ "$(uname)" == "Linux" ]]; then
  # Linux
  if [[ "$(uname -m)" == "aarch64" ]]; then
    PLATFORM="linux/arm64"
  else
    PLATFORM="linux/amd64"
  fi
else
  echo "Unsupported operating system"
  exit 1
fi


IMAGES_TO_PULL=(
  "provectuslabs/kafka-ui:v0.7.0"
  "apache/flink:1.20.1"
  "apache/kafka:3.9.0"
)

# Set the project name for Docker Compose grouping
PROJECT_NAME="63184-gruppe2-sensor-middleware"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "🚫 Docker is not running. Please start Docker and try again."
  exit 1
fi

# Pull images if not already present
for image_name in "${IMAGES_TO_PULL[@]}"; do
  if [[ "$(docker images -q $image_name 2> /dev/null)" == "" ]]; then
    echo "⬇️  Pulling image $image_name for $PLATFORM..."
    docker pull --platform $PLATFORM $image_name
  else
    echo "✅ Image $image_name is already available."
  fi
done


# Start Docker Compose services
echo "🚀 Starting Docker Compose services..."
docker-compose -f 63184-docker-compose.yml -p $PROJECT_NAME up -d
