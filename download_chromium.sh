#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Set the Chromium source code directory
dir=~/benchmark/test-suites/chromium
mkdir -p $dir
cd $dir

# Check and install dependencies
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing..."
    sudo apt update && sudo apt install -y git
fi

# Download and configure depot_tools
if [ ! -d "depot_tools" ]; then
    echo "Cloning depot_tools..."
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
fi
export PATH="$dir/depot_tools:$PATH"

# Fetch Chromium source code
if [ ! -d "src" ]; then
    echo "Fetching Chromium source code..."
    fetch --nohooks chromium
fi

cd src

# Synchronize dependencies
echo "Running gclient sync..."
gclient sync

echo "Chromium source code has been downloaded successfully!"

# Checkout a specific commit
commit_hash="e0cb393be5386dedf7f48735816377a7841fd5ff"  # Replace with the desired commit hash
echo "Checking out commit $commit_hash..."
git checkout $commit_hash
gclient sync --with_branch_heads --with_tags

echo "Chromium source code has been downloaded and checked out to commit $commit_hash successfully!"
