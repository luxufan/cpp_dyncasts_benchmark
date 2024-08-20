#!/usr/bin/env python3

import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    file_path = args.file
    f = open(args.file)
    data = json.load(f)
    tests = data['tests']['blink_perf.css']
    time = 0
    throughput = 0
    for t in tests:
        test = tests[t]
        artifacts = test['artifacts']
        measurements = artifacts['measurements.json']
        data_file = measurements[0]
        m_file = file_path[0:-len('test-results.json')] + data_file
        m_f = open(m_file)
        m_json = json.load(m_f)
        measurements = m_json['measurements']
        for tt in measurements:
            measurement = measurements[tt]
            unit = measurement['unit']
            sample = measurement['samples']
            count = sum(sample) / len(sample)
            if unit == 'ms':
                time += count
            else:
                throughput += count
    print(time)
    print(throughput)
