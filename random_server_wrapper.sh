#!/bin/bash

URL="https://random-number-mcp-server.manuelalejandromartinezf.workers.dev"

while IFS= read -r line; do
    # Forward the request to the HTTP server
    response=$(echo "$line" | curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d @-)
    
    # Return the response
    echo "$response"
done