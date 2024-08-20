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
    parser.add_argument("-m", "--metric", action="append", dest="metrics", default=[])
    parser.add_argument("base_thin",
                        help="Base thinlto file")
    parser.add_argument("compare_thin",
                        help="Compare thinlto file")
    parser.add_argument("base_full",
                        help="Base fulllto file")
    parser.add_argument("compare_full",
                        help="Compare fulllto file")

    rename_map = {'blender': 'Blender', 'chrome': 'Chromium', 'povray': 'POV-Ray', 'solc':'Solidity', 'envoy-static':'Envoy', 'opt':'LLVM', '471.omnetpp':'OMNeT++', '447.dealII':'deal.II', 'd8':'V8', 'z3':'Z3'}
    rows = ['Blender', 'Chromium', 'deal.II', 'Envoy', 'LLVM', 'OMNeT++', 'POV-Ray', 'Solidity', 'V8', 'Z3']
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

    # Extract metrics

    metrics = [ 'compile_time' ]

    base_thin_metrics = base_thin_data[metrics]
    base_full_metrics = base_full_data[metrics]
    compare_thin_metrics = compare_thin_data[metrics]
    compare_full_metrics = compare_full_data[metrics]
    thin_improvement = ((base_thin_metrics - compare_thin_metrics) / base_thin_metrics) * 100
    full_improvement = ((base_full_metrics - compare_full_metrics) / base_full_metrics) * 100
    thin_improvement = -thin_improvement
    full_improvement = -full_improvement

    print(thin_improvement)
    print(full_improvement)
    improvement = pd.DataFrame()
    improvement.insert(0, "LTO", full_improvement)
    improvement.insert(1, "ThinLTO", thin_improvement, allow_duplicates=True)
    improvement = improvement.round(2)

    colors = {'LTO': 'xkcd:azure', 'ThinLTO': 'darksalmon'}
    edgecolors = {'LTO': 'darkblue', 'ThinLTO': 'black'}
    width = 0.3
    multiplier = 0
    plt.rcParams.update({'font.size': 18})
    fig, ax1 = plt.subplots(figsize=(13, 6.7))
    fig.subplots_adjust(hspace=0.08, bottom=0.2)

    for spine in ax1.spines.values():
        spine.set_color('xkcd:almost black')
        spine.set_linewidth(1.5)

    ax1.set_title("Compile Time")
    for spine in ax1.spines.values():
        spine.set_color('xkcd:almost black')
        spine.set_linewidth(2)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    x = np.arange(len(improvement.index))
    kwargs = dict(linewidth=1.8, edgecolor='black', visible=True)
    for col in improvement.columns:
        offset = (width) * multiplier
        labels = improvement[col].round(2).astype('str') + '%'
        rects = ax1.bar(x + offset, improvement[col], width, label=col, linewidth=1.5, color=colors[col], edgecolor=edgecolors[col])
        #ax1.bar_label(rects, labels=labels, padding=3)
        #ax2.bar(x + offset, improvement[col], width, label=col, **kwargs)
        #ax1.bar_label(rects, padding = 3)
        multiplier += 1

    fontsize = 20
    ax1.set_ylim(-0.5, 5)
    ax1.set_ylabel('', fontsize=fontsize)
    ax1.set_xticks(x + width/2, improvement.index, fontsize=fontsize)
    ax1.tick_params(axis='x', labelrotation=20)
    # add percentage symbol to y ticks
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{0}%'.format(round(x)) for x in vals], fontsize=fontsize)

    ax1.legend(loc="upper right", ncols=2, fontsize="20")
    #plot = base_improvement.plot.bar(rot=0, figsize=(46, 30))
    d = .5
    plt.show()
    plt.savefig("compiletime.tocrop.pdf")

if __name__ == "__main__":
    main()
