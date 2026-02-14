#!/usr/bin/env bash

# update resources/match-rules.tab with the latest version data 
# from the burp-suite-error-message-checks repository
curl -fsSL https://raw.githubusercontent.com/augustd/burp-suite-error-message-checks/master/src/main/resources/burp/match-rules.tab -o yawast/resources/match-rules.tab

# basic sanity check: file must be non-empty and contain at least one tab delimiter
if [ ! -s yawast/resources/match-rules.tab ] || ! grep -q $'\t' yawast/resources/match-rules.tab; then
  echo "Error: Downloaded match-rules.tab appears invalid." >&2
  exit 1
fi
