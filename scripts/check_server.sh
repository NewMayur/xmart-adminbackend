#!/bin/bash

# Local API endpoint to check
URL="http://127.0.0.1:5000/check-server"

# Timeout duration in seconds
TIMEOUT=2

# Command to reload the local server
RELOAD_COMMAND="python server.py"

# Function to reload the server
reload_server() {
    echo "$(date): Timeout occurred or server is down. Reloading the server"
    pkill -f "$RELOAD_COMMAND"  # Kill the running server process
    nohup $RELOAD_COMMAND &> server.log &  # Restart the server in the background and log output
    echo "$(date): Server reloaded"
}

while true; do
    # Check the response time of the API and capture the response
    response=$(curl -s -w "%{time_total}" -o response_body.txt --max-time $TIMEOUT $URL)
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        # If curl failed (exit code not 0), it means the server is not running or not reachable
        echo "$(date): Server not reachable or request timed out"
        reload_server
    else
        # Convert the response time to an integer (in milliseconds)
        response_time=$(echo $response | awk '{print int($1*1000)}')
        
        # Log response time
        echo "$(date): Response time: ${response_time}ms"
        
        # Check if the response time exceeds the timeout
        if [ $response_time -ge $((TIMEOUT*1000)) ]; then
            reload_server
        else
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
