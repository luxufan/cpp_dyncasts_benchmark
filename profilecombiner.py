#!/usr/bin/env python3
import json
import sys
import os.path

def create_init_benchmark_json():
    stats = {}
    stats["__version__"] = [18, 0, 0]
    stats["elapsed"] = 0.0
    stats["tests"] = []
    return stats

def combine_profile(binary_name, profile, merged_profile):
    all_tests = merged_profile["tests"]
    profile_data = {}
    profile_data["name"] = binary_name

    pf = open(profile, 'r')
    lines = pf.readlines()

    for l in lines:
        collon_pos = l.find(':')
        profile_data[l[:collon_pos]] = l[collon_pos + 2: -1]

    all_tests.append(profile_data)

if __name__ == "__main__":
    result_dict = create_init_benchmark_json()

    for i in range(1, len(sys.argv), 2):
        combine_profile(sys.argv[i], sys.argv[i + 1], result_dict)

    with open('profile.json', 'w') as f:
        json.dump(result_dict, f, indent=4)
