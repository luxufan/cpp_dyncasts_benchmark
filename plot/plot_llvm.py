#!/usr/bin/env python3

import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms

def getmemory(data):
    return json.load(open(data))['tests'][0]['metrics']['test_memory']

def getsize(data):
    return json.load(open(data))['tests'][0]['metrics']['size']

def gettime(data):
    return json.load(open(data))['tests'][0]['metrics']['test_time']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="analysis_chrome.py")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_argument("origin_thinlto",
                        help="Base thinlto file")
    parser.add_argument("origin_fulllto",
                        help="Compare thinlto file")
    parser.add_argument("poly_thinlto",
                        help="Base fulllto file")
    parser.add_argument("poly_fulllto",
                        help="Compare fulllto file")
    parser.add_argument("virtual_thinlto",
                        help="Base thinlto file")
    parser.add_argument("virtual_thinlto_dyncastopt",
                        help="Base thinlto file")
    parser.add_argument("virtual_fulllto",
                        help="Base thinlto file")
    parser.add_argument("virtual_fulllto_dyncastopt",
                        help="Base thinlto file")
    parser.add_argument("diff_thinlto",
                        help="Base thinlto file")
    parser.add_argument("diff_thinlto_dyncastopt",
                        help="Base thinlto file")
    parser.add_argument("diff_fulllto",
                        help="Base thinlto file")
    parser.add_argument("diff_fulllto_dyncastopt",
                        help="Base thinlto file")
    args = parser.parse_args()

    thinlto_time = [gettime(i) for i in [args.poly_thinlto, args.virtual_thinlto, args.virtual_thinlto_dyncastopt, args.diff_thinlto, args.diff_thinlto_dyncastopt]]
    thinlto_time = [(i - gettime(args.origin_thinlto)) / gettime(args.origin_thinlto) * 100 for i in thinlto_time]
    print(thinlto_time)
    lto_time = [gettime(i) for i in [args.poly_fulllto, args.virtual_fulllto, args.virtual_fulllto_dyncastopt, args.diff_fulllto, args.diff_fulllto_dyncastopt]]
    lto_time = [(i - gettime(args.origin_fulllto)) / gettime(args.origin_fulllto) * 100 for i in lto_time]

    lto_memory = [getmemory(i) for i in [args.poly_fulllto, args.virtual_fulllto, args.virtual_fulllto_dyncastopt, args.diff_fulllto, args.diff_fulllto_dyncastopt]]
    lto_memory = [(i - getmemory(args.origin_fulllto)) / getmemory(args.origin_fulllto) * 100 for i in lto_memory]

    thinlto_memory = [getmemory(i) for i in [args.poly_thinlto, args.virtual_thinlto, args.virtual_thinlto_dyncastopt, args.diff_thinlto, args.diff_thinlto_dyncastopt]]
    thinlto_memory = [(i - getmemory(args.origin_thinlto)) / getmemory(args.origin_thinlto) * 100 for i in thinlto_memory]

    thinlto_size = [getsize(i) for i in [args.poly_thinlto, args.virtual_thinlto, args.virtual_thinlto_dyncastopt, args.diff_thinlto, args.diff_thinlto_dyncastopt]]
    thinlto_size = [(i - getsize(args.origin_thinlto)) / getsize(args.origin_thinlto) * 100 for i in thinlto_size]
    lto_size = [getsize(i) for i in [args.poly_fulllto, args.virtual_fulllto, args.virtual_fulllto_dyncastopt, args.diff_fulllto, args.diff_fulllto_dyncastopt]]
    lto_size = [(i - getsize(args.origin_fulllto)) / getsize(args.origin_fulllto) * 100 for i in lto_size]

    labels = ['polymorphic', 'virtual', 'virtual + opt', 'diff', 'diff + opt']

    plt.rcParams.update({'font.size': 17})

    width = 0.25
    fontsize = 18
    x = np.arange(5)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    fig.subplots_adjust(hspace=0.3, wspace=0.4, bottom=0.26, top=0.82)

    thin_bar_color = "darksalmon"
    thin_edge_color = 'black'
    lto_bar_color = 'xkcd:azure'
    lto_edge_color = 'black'


    ax1.set_title("Run time overhead", y=1.15, fontsize=18)
    ax1.text(0.5, 30.5, '>350%')
    ax1.text(2.6, 30.5, '>550%')
    ax1.set_ylim(0, 30)
    rects = ax1.bar(x, lto_time, width, edgecolor=lto_edge_color, linewidth=1.5, color=lto_bar_color)
    ax1.bar(x + width, thinlto_time, width, edgecolor=thin_edge_color, linewidth=1.5, color=thin_bar_color)

    ax1.set_xticks(x + width/2, labels, fontsize=17)
    ax1.set_yticklabels(['{0}%'.format(round(x, 1)) for x in ax1.get_yticks()], fontsize=fontsize)
    #ax1.set_ylabel('Miliseconds', fontsize=fontsize)
    ax1.tick_params(axis='x', labelrotation=15)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=25, ha='right', rotation_mode='anchor', fontsize=17)





    ### FullLTO running time
    ax2.set_title("Peak memory overhead", fontsize=18)
    bars = []
    bar = ax2.bar(x, lto_memory, width, edgecolor=lto_edge_color, linewidth=1.5, color=lto_bar_color)
    bars.append(bar)
    bar = ax2.bar(x + width, thinlto_memory, width, edgecolor=thin_edge_color, linewidth=1.5, color=thin_bar_color)
    ax2.set_xticks(x + width/2, labels, fontsize=fontsize)
    bars.append(bar)
    ax2.set_yticklabels(['{0}%'.format(round(x, 1)) for x in ax2.get_yticks()], fontsize=fontsize)
    #ax2.set_ylabel('Thousand runs', fontsize=fontsize)
    ax2.tick_params(axis='x', labelrotation=15)
    ax2.legend(bars, ['LTO', 'ThinLTO'], loc='upper center', ncols=2, fontsize='16', bbox_to_anchor=(0.5, 1.32))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=25, ha='right', rotation_mode='anchor', fontsize=17)

    ax3.set_title('Binary size overhead', fontsize=18)
    #ax3.set_ylim(46000, 52500)
    ax3.bar(x, lto_size, width, edgecolor=lto_edge_color, linewidth=1.5, color=lto_bar_color)
    ax3.bar(x + width, thinlto_size, width, edgecolor=thin_edge_color, linewidth=1.5, color=thin_bar_color)
    ax3.set_xticks(x + width/2, labels, fontsize=fontsize)
    ax3.set_yticklabels(['{0}%'.format(round(x, 1)) for x in ax3.get_yticks()], fontsize=fontsize)
    #ax3.set_ylabel('MegaByte', fontsize=fontsize)
    ax3.tick_params(axis='x', labelrotation=15)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=25, ha='right', rotation_mode='anchor', fontsize=17)

    plt.savefig("llvm.tocrop.pdf")
