#!/usr/bin/env python3

import json
from compare import read
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

def get_labels(bytes, kb, isfirst):
    label = []
    i = 0
    for byte in bytes:
        i += 1
        if i == 5 and isfirst:
            label.append('')
            continue
        if kb or (byte / (1024 * 1024) < 0.01):
            kbytes = round(byte / 1024, 1)
            s = ''
            if kbytes < 0.01:
                s = ''
                label.append(s)
                continue
            else:
                s = str(kbytes)
            label.append(s + 'KB')
        else:
            mb = byte / (1024 * 1024)
            roundnum = 1 if mb > 0.1 else 2
            mbytes = round(byte / (1024 * 1024), roundnum)
            s = ''
            if mbytes < 0.01:
                s = '0'
            else:
                s = str(mbytes)
            label.append(s + 'MB')
    return label

def main():
    parser = argparse.ArgumentParser(prog="plot_runtime_performance.py")
    parser.add_argument("base_thin",
                        help="Base thinlto file")
    parser.add_argument("compare_thin",
                        help="Compare thinlto file")
    parser.add_argument("base_full",
                        help="Base fulllto file")
    parser.add_argument("compare_full",
                        help="Compare fulllto file")
    rename_map = {'blender': 'Blender', 'chrome': 'Chromium-M', 'povray': 'POV-Ray', 'solc':'Solidity', 'envoy-static':'Envoy', 'opt':'LLVM-M', '471.omnetpp':'OMNeT++', '447.dealII':'deal.II', 'd8':'V8-M', 'z3':'Z3'}
    rows = ['Blender', 'Chromium-M', 'deal.II', 'Envoy', 'LLVM-M', 'OMNeT++', 'POV-Ray', 'Solidity', 'V8-M', 'Z3']
    config = parser.parse_args()
    base_thin_data = read(config.base_thin)
    base_thin_data.rename(index=rename_map, inplace=True)
    base_full_data = read(config.base_full)
    base_full_data.rename(index=rename_map, inplace=True)

    opt_thin_data = read(config.compare_thin)
    opt_thin_data.rename(index=rename_map, inplace=True)
    opt_full_data = read(config.compare_full)
    opt_full_data.rename(index=rename_map, inplace=True)

    base_thin_data = read(config.base_thin)
    base_thin_data.rename(index=rename_map, inplace=True)
    base_thin_data = base_thin_data.reindex(rows)
    base_full_data = read(config.base_full)
    base_full_data.rename(index=rename_map, inplace=True)
    base_full_data = base_full_data.reindex(rows)

    opt_thin_data = read(config.compare_thin)
    opt_thin_data.rename(index=rename_map, inplace=True)
    opt_thin_data = opt_thin_data.reindex(rows)
    opt_full_data = read(config.compare_full)
    opt_full_data.rename(index=rename_map, inplace=True)
    opt_full_data = opt_full_data.reindex(rows)
    opt_thin_slots_removed = opt_thin_data['rtti-clean.NumDeadVTables']
    opt_full_slots_removed = opt_full_data['rtti-clean.NumDeadVTables']
    #vtablebytes = opt_full_data['rtti-clean.NumVTableBytes']
    vtables = opt_full_data['rtti-count.NumZTV']
    opt_thin_slots_removed_percentage = opt_thin_slots_removed / vtables * 100
    opt_full_slots_removed_percentage = opt_full_slots_removed / vtables * 100

    base_full_pre_zti_zts = (base_full_data['rtti-count.NumPreZTI'] + base_full_data['rtti-count.NumPreZTS']).reindex(rows)
    base_full_zti_zts = (base_full_data['rtti-count.NumZTI'] + base_full_data['rtti-count.NumZTS']).reindex(rows)
    base_full_pre_zti_zts_bytes = (base_full_data['rtti-count.NumPreZTIBytes'] + base_full_data['rtti-count.NumPreZTSBytes']).reindex(rows)
    base_full_zti_zts_bytes = base_full_data['rtti-count.NumZTIBytes'] + base_full_data['rtti-count.NumZTSBytes']
    base_thin_pre_zti_zts = (base_thin_data['rtti-count.NumPreZTI'] + base_thin_data['rtti-count.NumPreZTS']).reindex(rows)
    base_thin_zti_zts = (base_thin_data['rtti-count.NumZTI'] + base_thin_data['rtti-count.NumZTS']).reindex(rows)
    base_thin_zti_zts_bytes = (base_thin_data['rtti-count.NumZTIBytes'] + base_thin_data['rtti-count.NumZTSBytes']).reindex(rows)
    opt_full_pre_zti_zts = (opt_full_data['rtti-count.NumPreZTI'] + opt_full_data['rtti-count.NumPreZTS']).reindex(rows)
    opt_full_zti_zts = (opt_full_data['rtti-count.NumZTI'] + opt_full_data['rtti-count.NumZTS']).reindex(rows)
    opt_full_pre_zti_zts_bytes = (opt_full_data['rtti-count.NumPreZTIBytes'] + opt_full_data['rtti-count.NumPreZTSBytes']).reindex(rows)
    opt_full_zti_zts_bytes = (opt_full_data['rtti-count.NumZTIBytes'] + opt_full_data['rtti-count.NumZTSBytes']).reindex(rows)
    opt_thin_pre_zti_zts = (opt_thin_data['rtti-count.NumPreZTI'] + opt_thin_data['rtti-count.NumPreZTS']).reindex(rows)
    opt_thin_zti_zts = (opt_thin_data['rtti-count.NumZTI'] + opt_thin_data['rtti-count.NumZTS']).reindex(rows)
    opt_thin_zti_zts_bytes = (opt_thin_data['rtti-count.NumZTIBytes'] + opt_thin_data['rtti-count.NumZTSBytes']).reindex(rows)

    base_full_remove_percentage = (base_full_pre_zti_zts - base_full_zti_zts) / base_full_pre_zti_zts * 100
    base_full_remove_bytes = base_full_pre_zti_zts_bytes - base_full_zti_zts_bytes
    base_thin_remove_bytes = base_full_pre_zti_zts_bytes - base_thin_zti_zts_bytes
    opt_full_remove_percentage = (opt_full_pre_zti_zts - opt_full_zti_zts) / opt_full_pre_zti_zts * 100
    base_thin_remove_percentage = (base_full_pre_zti_zts - base_thin_zti_zts) / base_full_pre_zti_zts * 100
    opt_thin_remove_percentage = (base_full_pre_zti_zts - opt_thin_zti_zts) / opt_full_pre_zti_zts * 100
    opt_full_remove_bytes = opt_full_pre_zti_zts_bytes - opt_full_zti_zts_bytes
    opt_thin_remove_bytes = opt_full_pre_zti_zts_bytes - opt_thin_zti_zts_bytes
    # print(opt_full_remove_bytes)
    # print(opt_thin_remove_bytes)
    # print(opt_thin_remove_bytes)
    bar_color = 'xkcd:azure'
    edge_color = 'darkblue'

    plt.rcParams.update({'font.size': 22})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 5))
    fig.subplots_adjust(wspace=0.11, hspace=0.1, bottom=0.25)

    # Plot with dyncastopt
    df = pd.DataFrame()
    df.insert(0, "LTO", opt_full_remove_percentage, True)
    #df.insert(1, "ThinLTO", opt_thin_remove_percentage, True)
    improvement = df
    print(improvement)

    width = 0.4
    multiplier = 0
    ax1.set_title("RTTI data removed", color='xkcd:almost black')
    for spine in ax1.spines.values():
        spine.set_color('xkcd:almost black')
        spine.set_linewidth(2)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    x = np.arange(len(improvement.index))
    for col in improvement.columns:
        offset = width * multiplier
        if col == 'ThinLTO':
            labels = get_labels(opt_thin_remove_bytes, False, False)
        else:
            labels = get_labels(opt_full_remove_bytes, False, False)
        rects = ax1.bar(x + offset, improvement[col], width, color=bar_color, label=col, edgecolor=edge_color, linewidth=2)
        ax1.bar_label(rects, labels=labels, color='xkcd:dark grey', padding=3, fontsize=18)
        #ax2.bar(x + offset, improvement[col], width, label=col, **kwargs)
        #ax1.bar_label(rects, padding = 3)
        multiplier += 1

    #ax1.set_ylabel('Removed')
    ax1.set_xticks(x, improvement.index, color='xkcd:black')
    ax1.set_ylim(0, 100)
    # add percentage symbol to y ticks
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{0}%'.format(round(x)) for x in vals], color='xkcd:black', fontsize=20)

    # plot vtable slots removement

    improvement = pd.DataFrame()
    improvement.insert(0, 'LTO', opt_full_slots_removed_percentage)
    width = 0.4
    multiplier = 0
    ax2.set_title("Vtables pruned", color='xkcd:almost black')

    for spine in ax2.spines.values():
        spine.set_color('xkcd:almost black')
        spine.set_linewidth(2)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    x = np.arange(len(improvement.index))
    for col in improvement.columns:
        offset = width * multiplier
        labels = improvement[col].round(2).astype('str') + '%'
        rects = ax2.bar(x + offset, improvement[col], width, label=col, color=bar_color, edgecolor=edge_color, linewidth=2)
        #ax1.bar_label(rects, labels=labels, padding=3)
        #ax2.bar(x + offset, improvement[col], width, label=col, **kwargs)
        #ax1.bar_label(rects, padding = 3)
        multiplier += 1

    #ax2.set_ylabel('vtables pruned')
    ax2.set_xticks(x, improvement.index, rotation=10)
    # add percentage symbol to y ticks
    vals = ax1.get_yticks()
    ax2.set_yticklabels(['{0}%'.format(round(x)) for x in vals], fontsize=20)



    #ax1.legend(loc="upper right", ncols=2, fontsize="15")
    #plot = base_improvement.plot.bar(rot=0, figsize=(46, 30))
    #ax1.tick_params(axis='x', labelrotation=18)
    #ax.tick_params(axis='x', labelrotation=18)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right', rotation_mode='anchor')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right', rotation_mode='anchor')
    plt.savefig('rtti_remove.tocrop.pdf')

    #
    df = pd.DataFrame()
    base_thin_remove_percentage['envoy-static'] = 0.0
    df.insert(0, "LTO", base_full_remove_percentage, True)
    #df.insert(1, "ThinLTO", base_thin_remove_percentage, True)
    improvement = df

    width = 0.4
    multiplier = 0
    plt.rcParams.update({'font.size': 22})
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.subplots_adjust(bottom=0.25)

    x = np.arange(len(improvement.index))
    for col in improvement.columns:
        offset = width * multiplier
        labels = []
        if col == 'LTO':
            labels = get_labels(base_full_remove_bytes, True, False)
        else:
            labels = get_labels(base_thin_remove_bytes, True, True)
        rects = ax.bar(x + offset, improvement[col], width, label=col, color=bar_color, edgecolor=edge_color, linewidth=2)
        #plt.rcParams.update({'font.size': 12})
        padding = 3
        if col == 'ThinLTO':
            padding = 3
        ax.bar_label(rects, labels=labels, padding=padding, color='xkcd:dark grey', fontsize=18)
        #ax2.bar(x + offset, improvement[col], width, label=col, **kwargs)
        #ax1.bar_label(rects, padding = 3)
        multiplier += 1

    #ax.set_ylabel('Removed', x=0)
    ax.set_xticks(x, improvement.index, color='xkcd:black')
    # add percentage symbol to y ticks
    vals = ax.get_yticks()
    ax.set_yticklabels(['{0}%'.format(x) for x in vals], fontsize=20)

    #ax.legend(loc="upper right", ncols=2, fontsize='17')
    ax.set_ylim(0, 3)
    #plot = base_improvement.plot.bar(rot=0, figsize=(46, 30))
    for spine in ax.spines.values():
        spine.set_color('xkcd:almost black')
        spine.set_linewidth(2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right', rotation_mode='anchor')
    plt.savefig('vanala_rtti.tocrop.pdf')
if __name__ == "__main__":
    main()
