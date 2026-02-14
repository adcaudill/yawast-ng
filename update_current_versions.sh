#!/usr/bin/env bash

# update resources/current_versions.json with the latest version data from the current_versions repository
curl -fsSL https://raw.githubusercontent.com/adcaudill/current_versions/main/current_versions.json -o yawast/resources/current_versions.json

# basic sanity check: file must be non-empty and contain valid JSON
if [ ! -s yawast/resources/current_versions.json ] || ! jq empty yawast/resources/current_versions.json > /dev/null 2>&1; then
  echo "Error: Downloaded current_versions.json appears invalid." >&2
  exit 1
fi
