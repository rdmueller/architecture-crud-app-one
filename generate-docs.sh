#!/bin/bash

# Generate documentation using docToolchain
# This script provides various options for generating documentation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_color "$RED" "Error: Docker is not installed"
        echo "Please install Docker from https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_color "$RED" "Error: Docker daemon is not running"
        echo "Please start Docker and try again"
        exit 1
    fi
}

# Function to generate HTML documentation
generate_html() {
    print_color "$YELLOW" "Generating HTML documentation..."
    ./dtcw generateHTML
    print_color "$GREEN" "HTML documentation generated in build/"
}

# Function to generate microsite
generate_microsite() {
    print_color "$YELLOW" "Generating microsite..."
    ./dtcw generateMicrosite
    print_color "$GREEN" "Microsite generated in build/microsite/"
}

# Function to clean build directory
clean_build() {
    print_color "$YELLOW" "Cleaning build directory..."
    rm -rf build/
    print_color "$GREEN" "Build directory cleaned"
}

# Function to preview documentation
preview_docs() {
    print_color "$YELLOW" "Starting documentation preview server..."
    docker-compose -f docToolchain-docker-compose.yml up preview
}

# Function to start live reload
live_reload() {
    print_color "$YELLOW" "Starting live reload mode..."
    docker-compose -f docToolchain-docker-compose.yml --profile dev up
}

# Main script
case "$1" in
    "html")
        check_docker
        generate_html
        ;;
    "microsite")
        check_docker
        generate_microsite
        ;;
    "all")
        check_docker
        generate_html
        generate_microsite
        ;;
    "clean")
        clean_build
        ;;
    "preview")
        check_docker
        generate_microsite
        preview_docs
        ;;
    "live")
        check_docker
        live_reload
        ;;
    *)
        echo "Usage: $0 {html|microsite|all|clean|preview|live}"
        echo ""
        echo "Commands:"
        echo "  html      - Generate HTML documentation"
        echo "  microsite - Generate microsite for GitHub Pages"
        echo "  all       - Generate both HTML and microsite"
        echo "  clean     - Clean the build directory"
        echo "  preview   - Generate microsite and start preview server on port 8080"
        echo "  live      - Start live reload mode for development"
        exit 1
        ;;
esac
