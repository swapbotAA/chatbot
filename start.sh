#!/bin/bash
PATH=$PATH:/usr/local/opt/python@3.9/bin/python3.9
export PATH


while true; do
    # Your script/command goes here
    nohup python3 /Users/aolin/Library/Python/3.9/lib/python/site-packages/rasa run --enable-api

    # Check the exit status of the last command
    if [ $? -ne 0 ]; then
        echo "Script crashed. Restarting..."
    else
        echo "Script completed successfully."
    fi

    # Sleep for a short duration before restarting
    sleep 5  # Adjust the sleep duration as needed
done