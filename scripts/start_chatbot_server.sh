# Function to start Docker containers
start_containers() {
    # Change directory to where the Compose file is located
    cd "$(dirname "$COMPOSE_FILE")" || exit

    # Start the containers defined in docker-compose-dropbot.yml (build if necessary)
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up --build
}

# Get the absolute path to the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Specify the path to your docker-compose-dropbot.yml file (assuming it's in the parent directory)
COMPOSE_FILE="$SCRIPT_DIR/../docker-compose.yml"

# Specify a unique project name for this Docker Compose run
PROJECT_NAME="assistant"

# Loop to restart containers on failure
while true; do
    # Stop the containers defined in docker-compose-dropbot.yml
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down

    # Call function to start containers
    start_containers

    # Check the exit code of the last executed command
    if [ $? -ne 0 ]; then
        echo "Containers crashed or exited with an error. Restarting..."
    else
        echo "Containers exited gracefully. Exiting loop."
        break
    fi

    # Delay before attempting to restart containers again
    sleep 5
done
