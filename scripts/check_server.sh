#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Function to reload the server
reload_server() {
    echo "$(date): Timeout occurred or server is down. Reloading the server"
    pkill -f "$RELOAD_COMMAND"  # Kill the running server process
    nohup $RELOAD_COMMAND &> server.log &  # Restart the server in the background and log output
    echo "$(date): Server reloaded"
}

while true; do
    # Check the response time of the API and capture the response
    response=$(curl -s -w "%{time_total} %{http_code}" -o response_body.txt --max-time $TIMEOUT $URL)
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        # If curl failed (exit code not 0), it means the server is not running or not reachable
        echo "$(date): Server not reachable or request timed out"
        reload_server
    else
        # Extract the response time and HTTP status code
        response_time=$(echo $response | awk '{print int($1*1000)}')
        http_code=$(echo $response | awk '{print $2}')
        
        # Log response time and HTTP status code
        echo "$(date): Response time: ${response_time}ms, HTTP status code: ${http_code}"
        
        # Check if the response time exceeds the timeout or if the HTTP status code is 502
        if [ $response_time -ge $((TIMEOUT*1000)) ] || [ "$http_code" -eq 502 ]; then
            reload_server
        else:
            # Print the response message from the server
            response_body=$(cat response_body.txt)
            echo "$(date): Server response: $response_body"
        fi
    fi

    # Clean up
    rm -f response_body.txt

    # Wait for a specified interval before the next check (e.g., 5 seconds)
    sleep 5
done
