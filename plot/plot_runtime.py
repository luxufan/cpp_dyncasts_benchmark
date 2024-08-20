#!/usr/bin/env python3

import json
from compare import read
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys

def main():
    parser = argparse.ArgumentParser(prog="plot_runtime_performance.py")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_argument("base_thin",
                        help="Base thinlto file")
    parser.add_argument("compare_thin",
                        help="Compare thinlto file")
    parser.add_argument("base_full",
                        help="Base fulllto file")
    parser.add_argument("compare_full",
                        help="Compare fulllto file")
    rename_map = {'blender': 'Blender', 'chrome': 'Chromium', 'povray': 'POV-Ray', 'solc':'Solidity', 'envoy-static':'Envoy', 'opt':'LLVM', '471.omnetpp':'OMNeT++', '447.dealII':'deal.II', 'd8':'V8-M', 'z3':'Z3'}
    rows = ['Blender', 'Chromium', 'deal.II', 'Envoy', 'LLVM', 'OMNeT++', 'POV-Ray', 'Solidity', 'V8-M', 'Z3']
    config = parser.parse_args()
    base_thin_data = read(config.base_thin)
    base_thin_data.rename(index=rename_map, inplace=True)
    base_thin_data = base_thin_data.reindex(rows)
    base_full_data = read(config.base_full)
    base_full_data.rename(index=rename_map, inplace=True)
    base_full_data = base_full_data.reindex(rows)

    compare_thin_data = read(config.compare_thin)
    compare_thin_data.rename(index=rename_map, inplace=True)
    compare_thin_data = compare_thin_data.reindex(rows)
    compare_full_data = read(config.compare_full)
    compare_full_data.rename(index=rename_map, inplace=True)
    compare_full_data = compare_full_data.reindex(rows)

    base_thin_metrics = base_thin_data["test_time"]
    base_full_metrics = base_full_data["test_time"]
    compare_thin_metrics = compare_thin_data["test_time"]
    compare_full_metrics = compare_full_data["test_time"]
    thin_improvement = ((base_thin_metrics - compare_thin_metrics) / base_thin_metrics) * 100
    full_improvement = ((base_full_metrics - compare_full_metrics) / base_full_metrics) * 100

    improvement = pd.DataFrame()
    improvement.insert(0, "LTO", full_improvement)
    improvement.insert(1, "ThinLTO", thin_improvement, allow_duplicates=True)
    improvement = improvement.round(2)

    improvement.iloc[3] = -improvement.iloc[3]

    improvement.drop('Chromium', inplace=True)
    improvement.drop('LLVM', inplace=True)
    improvement.drop('V8-M', inplace=True)
    lto_sum = improvement["LTO"].sum()
    print(lto_sum / 7)

    if config.verbose:
        print(improvement)

    width = 0.30
    multiplier = 0
    plt.rcParams.update({'font.size': 14})

    fig, ax2 = plt.subplots(1, 1, figsize=(9, 5))

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    fig.subplots_adjust(hspace=0.08, bottom=0.2)

    colors = {'LTO': 'xkcd:azure', 'ThinLTO': 'darksalmon'}
    edgecolors = {'LTO': 'black', 'ThinLTO': 'black'}
    x = np.arange(len(improvement.index))
    for col in improvement.columns:
        offset = width * multiplier
        ax2.bar(x + offset, improvement[col], width, label=col, color=colors[col], edgecolor='black', linewidth=1, align='edge')
        multiplier += 1

    fontsize = 20
    ax2.set_ylim(-1, 6)
    ax2.set_ylabel('', labelpad=10, fontsize=fontsize, y=0.7)
    ax2.set_xticks(x + width, improvement.index, fontsize=fontsize)
    ax2.set_title('Run-time Performance', fontsize=fontsize)

    # set y labels
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{0}%'.format(round(x)) for x in vals], fontsize=18)

    ax2.tick_params(axis='x', labelrotation=18)

    d = .5
    leg = plt.legend(loc='upper left')
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=18.5,
              linestyle="none", color='k', mec='k', mew=2, clip_on=False)
    plt.show()
    plt.savefig("runtime.tocrop.pdf")

if __name__ == "__main__":
    main()
