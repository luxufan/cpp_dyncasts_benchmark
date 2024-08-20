#!/bin/bash

set -e  # Exit immediately if a command fails

export PATH="$PATH:~/.foundry/bin"
# Define repositories and their specific commit hashes
declare -A repos=(
    ["z3"]="https://github.com/Z3Prover/z3.git d7931b93425e5db3dbd0366f1dbdb843313f3fb4"
    ["solidity"]="https://github.com/ethereum/solidity.git 90c0fbb2eaafae95fae7785e4de5dfb43d5ddce3"
    ["povray"]="https://github.com/POV-Ray/povray.git 76a804d18a30a1dbb0afbc0070b62526715571eb"
    ["blender"]="https://github.com/blender/blender.git 396f546c9d8298d74c3f98df38bbcfa6c92ee5b9"
    ["envoy"]="https://github.com/envoyproxy/envoy.git faf1db422195010e42acf352e5366c27dbeb8685"
    ["llvm-project"]="git@github.com:luxufan/llvm.git 51958c87a955702693be931a7d2d535860c96d2f"
)

# Define repositories that require extra setup commands
declare -A extra_commands=(
    ["solidity"]="test/benchmarks/external-setup.sh"
    ["povray"]="unix/prebuild.sh"
#    ["blender"]="./build_files/utils/make_update.py --use-linux-libraries && git clone https://projects.blender.org/blender/blender-benchmarks.git tests/benchmarks && tests/performance/benchmark.py init && cp $HOME/benchmark/test-data/config.py $HOME/benchmark/test-suites/benchmark/default/config.py"
)

# Set base directory for cloning repositories
base_dir=$HOME/benchmark/test-suites
mkdir -p "$base_dir"

for repo_name in "${!repos[@]}"; do
    repo_info=(${repos[$repo_name]})
    repo_url=${repo_info[0]}
    commit_hash=${repo_info[1]}
    
    repo_dir="$base_dir/$repo_name"
    
    if [ ! -d "$repo_dir" ]; then
        echo "Cloning $repo_name..."
        git clone "$repo_url" "$repo_dir"
    else
        echo "$repo_name already exists. Skipping clone..."
    fi

    cd "$repo_dir"

    echo "Checking out commit $commit_hash..."
    git fetch origin
    git checkout "$commit_hash"

    # Run extra setup commands if needed
    if [[ -n "${extra_commands[$repo_name]}" ]]; then
        echo "Running extra setup for $repo_name..."
        eval "${extra_commands[$repo_name]}"
    fi

    echo "$repo_name is ready at commit $commit_hash."
    cd "$base_dir"
done

echo "All repositories have been checked out successfully!"

