#!/bin/bash -e
image_name=my_etl
image_tag=latest
dockerhub_name="$(echo "$DOCKERHUB_NAME")"
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker login
docker tag "${full_image_name}" "${dockerhub_name}"/"${full_image_name}"
docker push "${dockerhub_name}"/"${full_image_name}"

# Output the strict image name, which contains the sha256 image digest
# docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"