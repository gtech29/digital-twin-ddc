#!/bin/bash

# Base directory containing your Dockerfiles
BASE_DIR="./docker"

# Map of directory name => image name
declare -A services=(
  ["plc"]="plc"
  ["sensors"]="sensor"
  ["trane"]="trane"
  ["dnp3"]="dnp3"
  ["jensys"]="jensys"
  ["broker"]="mqtt-broker"
  ["dashboard"]="dashboard"
)

for dir in "${!services[@]}"; do
  image="${services[$dir]}"
  
  echo " Building image for $image from $BASE_DIR/$dir..."
  docker build -t "$image:latest" "$BASE_DIR/$dir" || { echo "Build failed for $image"; exit 1; }

  echo " Saving image $image..."
  docker save "$image:latest" -o "${image}.tar" || { echo "Save failed for $image"; exit 1; }

  echo " Importing image $image into k3s..."
  sudo ctr images import "${image}.tar" || { echo " Import failed for $image"; exit 1; }

  echo " $image image built and imported successfully."
done

echo "All images built and loaded into k3s!"
