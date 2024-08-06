#!/bin/bash

# Check if postfix is running
postfix_status=$(pgrep -x "master" > /dev/null 2>&1 && echo "running" || echo "not running")

# Check if Flask app is running
flask_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/queue)

if [ "$postfix_status" == "running" ] && [ "$flask_status" == "200" ]; then
  echo "Postfix and Flask are running"
  exit 0
else
  echo "Postfix or Flask is not running"
  exit 1
fi
