#!/usr/bin/env python3
import json
from compare import read
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

def main():
    parser = argparse.ArgumentParser(prog="plot_addresspoints_candidates.py")
    parser.add_argument("file", help="statistics file")
    config = parser.parse_args()
    stats = read(config.file)
    plt.rcParams.update({'font.size': 14})
    fig, axes = plt.subplots(2, 5)
    fig.set_figheight(5.2)
    fig.set_figwidth(16)
    fig.subplots_adjust(hspace=0.15, wspace=0.40)
    col_names = ["dyncastopt.NumLeafNodes", "dyncastopt.NumTwoCandidates", "dyncastopt.NumThreeCandidates", "dyncastopt.NumMoreThanThreeCandidates", "dyncastopt.NumRangeCheck"]
    colors = {"LeafNodes": "tab:orange", "TwoCandidates":'tab:blue', 'ThreeCandidates':'green', 'MoreThanTwoCandidates':'tab:red', 'RangeCheck':'purple', 'Failed':'black'}
    candidates = stats[col_names]
    nan_index = np.isnan(candidates)
    candidates[nan_index] = 0
    rename_map = {'blender': 'Blender', 'chrome': 'Chromium-M', 'povray': 'POV-Ray', 'solc':'Solidity', 'envoy-static':'Envoy', 'opt':'LLVM-M', '471.omnetpp':'OMNeT++', '447.dealII':'deal.II', 'd8':'V8-M', 'z3':'Z3'}
    rows = ['Blender', 'Chromium-M', 'deal.II', 'Envoy', 'LLVM-M', 'OMNeT++', 'POV-Ray', 'Solidity', 'V8-M', 'Z3']
    candidates.rename(index=rename_map, inplace=True)
    candidates = candidates.reindex(rows)
    num_dyncasts = stats["dyncastopt.NumDynCast"]
    num_dyncasts.rename(index=rename_map, inplace=True)
    num_optimized = candidates.sum(axis=1)
    num_failed = num_dyncasts - num_optimized
    candidate = pd.DataFrame()
    candidate.insert(0, "dyncastopt.NumLeafNodes", candidates['dyncastopt.NumLeafNodes'])
    candidate.insert(1, "dyncastopt.NumTwoCandidates", candidates['dyncastopt.NumTwoCandidates'])
    candidate.insert(2, 'dyncastopt.NumMoreThanTwoCandidates', candidates['dyncastopt.NumThreeCandidates'] + candidates['dyncastopt.NumMoreThanThreeCandidates'])
    candidate.insert(3, 'dyncastopt.NumRangeCheck', candidates['dyncastopt.NumRangeCheck'])
    candidate.insert(4, 'dyncastopt.NumFailed', num_failed)
    print(num_failed)
    candidates = candidate
    print(candidates)

    print(len(axes))
    axes_list = []
    for x in axes:
        for ax in x:
            axes_list.append(ax)

    width = 0.4

    rmprefix = lambda s: s[len('dyncastopt.Num'):]
    for i in range(10):
        labels = []
        title = candidates.index[i]
        #print(candidates.index[i])
        row = candidates.loc[candidates.index[i]]
        testsuite = candidates.index[i]
       # row = row.sort_values(ascending=False)
        ii = 0
        color = []
        data = []
        for n in row:
            name = rmprefix(candidates.columns[ii])
            color.append(colors[name])
            #print(name)
            if name == 'LeafNodes':
                labels.append('1')
            elif name == 'TwoCandidates':
                labels.append('2')
            elif name == 'ThreeCandidates':
                labels.append('3')
            elif name == 'MoreThanTwoCandidates':
                labels.append('>2')
            elif name == 'RangeCheck':
                labels.append('rc')
            elif name == 'Failed':
                labels.append('dyn')
            elif name == 'FiveCandidates':
                labels.append('5')
            elif name == 'SixCandidates':
                labels.append('6')
            elif name == 'SevenCandidates':
                labels.append('7')
            elif name == 'MoreThanSevenCandidates':
                labels.append('>7')
            else:
                labels.append(name[:-len('Candidates')])
            data.append(n)
            ii += 1
        if testsuite == 'OMNeT++' or testsuite == 'deal.II':
            axes_list[i].set_yticks(np.arange(0, 14, step=3))
        print(data)
        print(labels)
        axes_list[i].bar(labels, data, width, color=color, linewidth=1, edgecolor='black')
        axes_list[i].set_xlim(-1, 5)
        if testsuite == 'POV-Ray':
          axes_list[i].set_title(testsuite, x=0.32, y=1.0, pad=-20, fontsize=16)
        elif testsuite == 'OMNeT++':
          axes_list[i].set_title(testsuite, x=0.6, y=1.0, pad=-20, fontsize=16)
        elif testsuite == 'Chromium-M':
          axes_list[i].set_title(testsuite, x=0.61, y=1.0, pad=-20, fontsize=16)
        elif testsuite == 'deal.II':
          axes_list[i].set_title(testsuite, x=0.6, y=1.0, pad=-20, fontsize=16)
        else:
          axes_list[i].set_title(testsuite, y=1.0, pad=-20, fontsize=16)
        axes_list[i].tick_params(axis='x', which='major', pad=3)

    plt.show()
    plt.savefig("profile.tocrop.pdf")

if __name__ == "__main__":
    main()
