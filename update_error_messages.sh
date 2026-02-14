#!/usr/bin/env bash

# update resources/match-rules.tab with the latest version data 
# from the burp-suite-error-message-checks repository
curl -sL https://raw.githubusercontent.com/augustd/burp-suite-error-message-checks/master/src/main/resources/burp/match-rules.tab -o yawast/resources/match-rules.tab
