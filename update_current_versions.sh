#!/usr/bin/env bash

# update resources/current_versions.json with the latest version data from the current_versions repository
curl -sL https://raw.githubusercontent.com/adcaudill/current_versions/main/current_versions.json -o yawast/resources/current_versions.json
