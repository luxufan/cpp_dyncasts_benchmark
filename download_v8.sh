#!/bin/bash

# Define variables
V8_REPO="https://chromium.googlesource.com/v8/v8.git"
CHROMIUM_REPO="https://chromium.googlesource.com/chromium/src.git"
V8_COMMIT="14df7707ca206d41f8c022ce33c327d3dbbcc5e9"  # Replace with the desired V8 commit hash
CHROMIUM_COMMIT="e0cb393be5386dedf7f48735816377a7841fd5ff"  # Replace with the desired Chromium commit hash
WORK_DIR="$HOME/benchmark/test-suites"

# Create working directory
echo "Creating working directory: $WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR" || { echo "Failed to create or access working directory"; exit 1; }

# Install depot_tools if not already installed
if ! command -v fetch &> /dev/null; then
    echo "Installing depot_tools..."
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    export PATH="$WORK_DIR/depot_tools:$PATH"
else
    echo "depot_tools is already installed."
fi

# Download V8 source code
echo "Downloading V8 source code..."
mkdir v8
cd v8
fetch --nohooks v8
cd v8
./build/install-build-deps.sh
gclient runhooks

# Checkout to the specific V8 commit
echo "Checking out V8 to commit: $V8_COMMIT"
git checkout "$V8_COMMIT" || { echo "Failed to checkout V8 commit"; exit 1; }

gclient sync
