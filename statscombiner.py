#!/usr/bin/env python3
#
import json
import sys
import os.path
import argparse

def create_init_benchmark_json():
    stats = {}
    stats["__version__"] = [18, 0, 0]
    stats["elapsed"] = 0.0
    stats["tests"] = []
    return stats

def combine_stats(stats, bench_result):
    all_tests = bench_result["tests"]

    binary_name = stats[stats.rfind('/') + 1:-6]
    binary_path = os.path.dirname(stats) + "/" + binary_name
    new_stats_dict = {"code": "PASS", "elapsed" : 0.0, "metrics" : {}, "shortname": binary_name, "name": binary_name, "output": ""}

    metrics = new_stats_dict["metrics"]
    metrics["size"] = os.path.getsize(binary_path)
    with open(stats) as json_data:
        d = json.load(json_data)
        for metric in d:
            metrics[metric] = d[metric]

    all_tests.append(new_stats_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base')
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()

    print(args.filenames)


    result_dict = {}
    if args.base:
        f = open(args.base)
        result_dict = json.load(f)
    else:
        result_dict = create_init_benchmark_json()

    for f in args.filenames:
        combine_stats(f, result_dict)

    with open('result.json', 'w') as f:
        json.dump(result_dict, f, indent=4)
