#!/usr/bin/env python3
#
import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms

ignore_list = ['AttributeDescendantSelector', 'ClassDescendantSelector', 'ClassInvalidation', 'FocusUpdate', 
               'ModifySelectorText', 'PseudoClassSelectors', 'SelectorCountScaling', 'HasDescendantInvalidation', 'HasDescendantInAncestorPositionInvalidation',
               'HasDescendantInvalidationAllSubjects', 'HasDescendantInvalidationMultipleSubjects', 'HasDescendantInvalidationWith1NonMatchingHasRule',
               'HasDescendantInvalidationWithMultipleNonMatchingHasRules', 'HasDescendantInvalidationWithoutNonMatchingHasRule',
               'CSSPropertySetterGetter', 'CSSPropertySetterGetterMethods', 'CSSPropertyUpdateValue', 'HasInvalidationFiltering',
               'HasSiblingDescendantInvalidation', 'HasSiblingDescendant', 'HasSiblingDescendantInvalidationAllSubjects']

origin_labels = set()
thinlto_dyncastopt_labels = set()
sanitize_labels = set()
thinlto_labels = set()

lto_origin_labels = set()
lto_dyncastopt_labels = set()
lto_sanitize_labels = set()
lto_labels = set()

def gettime(data):
    return data['tests'][0]['metrics']['test_time']

def getsize(data):
    return data['tests'][0]['metrics']['size']

def getthroughput(data):
    return data['tests'][0]['metrics']['test_throughput']

def getmemory(data):
    return data['tests'][0]['metrics']['test_memory']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="analysis_chrome.py")
    parser.add_argument("thinlto",
                        help="Base thinlto file")
    parser.add_argument("thinlto_dyncastopt",
                        help="Compare thinlto file")
    parser.add_argument("fulllto",
                        help="Base fulllto file")
    parser.add_argument("fulllto_dyncastopt",
                        help="Compare fulllto file")
    parser.add_argument("origin_thin",
                        help="Base thinlto file")
    parser.add_argument("origin_full",
                        help="Compare thinlto file")
    parser.add_argument("sanitize_thin",
                        help="Base fulllto file")
    parser.add_argument("sanitize_full",
                        help="Compare fulllto file")
    args = parser.parse_args()

    print(args.thinlto)
    thinlto = json.load(open(args.thinlto))
    thinlto_dyncastopt = json.load(open(args.thinlto_dyncastopt))
    fulllto = json.load(open(args.fulllto))
    fulllto_dyncastopt = json.load(open(args.fulllto_dyncastopt))
    origin_thin = json.load(open(args.origin_thin))
    origin_full = json.load(open(args.origin_full))
    sanitize_thin = json.load(open(args.sanitize_thin))
    sanitize_full = json.load(open(args.sanitize_full))

    # find label
    #

    thinlto_ms = gettime(thinlto)
    lto_ms = gettime(fulllto)
    thinlto_unitless = getthroughput(thinlto)
    lto_unitless = getthroughput(fulllto)
    thinlto_mem = getmemory(thinlto)
    lto_mem = getmemory(fulllto)
    origin_ms = gettime(origin_thin)
    lto_origin_ms = gettime(origin_full)
    origin_unitless = getthroughput(origin_thin)
    lto_origin_unitless = getthroughput(origin_full)
    origin_mem = getmemory(origin_thin)
    lto_origin_mem = getmemory(origin_full)
    thinlto_dyncastopt_ms = gettime(thinlto_dyncastopt)
    lto_dyncastopt_ms = gettime(fulllto_dyncastopt)
    thinlto_dyncastopt_unitless = getthroughput(thinlto_dyncastopt)
    lto_dyncastopt_unitless = getthroughput(fulllto_dyncastopt)
    thinlto_dyncastopt_mem = getmemory(thinlto_dyncastopt)
    lto_dyncastopt_mem = getmemory(fulllto_dyncastopt)
    sanitize_ms = gettime(sanitize_thin)
    lto_sanitize_ms = gettime(sanitize_full)
    sanitize_unitless = getthroughput(sanitize_thin)
    lto_sanitize_unitless = getthroughput(sanitize_full)
    sanitize_mem = getmemory(sanitize_thin)
    lto_sanitize_mem = getmemory(sanitize_full)

    labels = ['dyn cast', 'dyn cast + opt', 'sanitizer']
    names = set()
    count = 1
    origin_ms = origin_ms / count
    origin_unitless = origin_unitless / count
    thinlto_ms = thinlto_ms / count
    thinlto_unitless = thinlto_unitless / count
    thinlto_dyncastopt_ms = thinlto_dyncastopt_ms / count
    thinlto_dyncastopt_unitless = thinlto_dyncastopt_unitless / count
    sanitize_ms = sanitize_ms / count
    sanitize_unitless = sanitize_unitless / count

    lto_origin_ms = lto_origin_ms / count
    lto_origin_unitless = lto_origin_unitless / count
    lto_ms = lto_ms / count
    lto_unitless = lto_unitless / count
    lto_dyncastopt_ms = lto_dyncastopt_ms / count
    lto_dyncastopt_unitless = lto_dyncastopt_unitless / count
    lto_sanitize_ms = lto_sanitize_ms / count
    lto_sanitize_unitless = lto_sanitize_unitless / count

    print('origin_ms:', origin_ms)
    print('origin_unitless:', origin_unitless)
    print('thinlto_ms:', thinlto_ms)
    print('thinlto_unitless:', thinlto_unitless)
    print('thinlto_dyncastopt_ms:', thinlto_dyncastopt_ms)
    print('thinlto_dyncastopt_unitless:', thinlto_dyncastopt_unitless)
    print('sanitize_ms:', sanitize_ms)
    print('sanitize_unitless:', sanitize_unitless)

    print('lto_origin_ms:', lto_origin_ms)
    print('lto_origin_unitless:', lto_origin_unitless)
    print('lto_ms:', lto_ms)
    print('lto_unitless:', lto_unitless)
    print('lto_dyncastopt_ms:', lto_dyncastopt_ms)
    print('lto_dyncastopt_unitless:', lto_dyncastopt_unitless)
    print('lto_sanitize_ms:', lto_sanitize_ms)
    print('lto_sanitize_unitless:', lto_sanitize_unitless)

    width = 0.3
    runtime_tests = [thinlto_ms, thinlto_dyncastopt_ms, sanitize_ms]
    runtime_tests = [(i - origin_ms) / origin_ms * 100 for i in runtime_tests]
    lto_runtime_tests = [lto_ms, lto_dyncastopt_ms, lto_sanitize_ms]
    lto_runtime_tests = [(i - lto_origin_ms) / lto_origin_ms * 100 for i in lto_runtime_tests]
    throughput_tests = [thinlto_unitless, thinlto_dyncastopt_unitless, sanitize_unitless]
    throughput_tests = [(i - origin_unitless) / origin_unitless * 100 for i in throughput_tests]
    print(throughput_tests)
    lto_throughput_tests = [lto_unitless, lto_dyncastopt_unitless, lto_sanitize_unitless]
    lto_throughput_tests = [(i - lto_origin_unitless ) * 100 / lto_origin_unitless for i in lto_throughput_tests]

    memory_tests = [thinlto_mem, thinlto_dyncastopt_mem, sanitize_mem]
    memory_tests = [(i - origin_mem) / origin_mem * 100 for i in memory_tests]
    lto_memory_tests = [lto_mem, lto_dyncastopt_mem, lto_sanitize_mem]
    lto_memory_tests = [(i - lto_origin_mem) / lto_origin_mem * 100 for i in lto_memory_tests]
    print("lto_throught:", lto_throughput_tests)
    binary_size = [getsize(thinlto), getsize(thinlto_dyncastopt), getsize(sanitize_thin)]
    binary_size = [(i - getsize(origin_thin)) / getsize(origin_thin) * 100 for i in binary_size]
    lto_binary_size = [getsize(fulllto), getsize(fulllto_dyncastopt), getsize(sanitize_full)]
    lto_binary_size = [(i - getsize(origin_full)) / getsize(origin_full) * 100 for i in lto_binary_size]
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(17, 5))
    fig.subplots_adjust(right=0.8, hspace=0.3, wspace=0.4, bottom=0.26, top=0.82)
    fontsize = 17
    x = np.arange(3)

    thin_bar_color = "darksalmon"
    thin_edge_color = 'black'
    lto_bar_color = 'xkcd:azure'
    lto_edge_color = 'black'

    plt.rcParams.update({'font.size': 17})
    ### ThinLTO running time
    ax1.set_title("Run time overhead")
    #ax1.set_ylim(2000, 2800)
    ax1.bar(x, lto_runtime_tests, width, edgecolor=lto_edge_color, linewidth=1, color=lto_bar_color)
    ax1.bar(x + width, runtime_tests, width, edgecolor=thin_edge_color, linewidth=1, color=thin_bar_color)

    ax1.set_xticks(x + width/2, labels, fontsize=17)
    ax1.set_yticklabels(['{0}%'.format(round(x)) for x in ax1.get_yticks()], fontsize=fontsize)
    #ax1.set_ylabel('Miliseconds', fontsize=fontsize)
    ax1.tick_params(axis='x', labelrotation=25)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=15, ha='right', rotation_mode='anchor', fontsize=17)
    # dx = -25/72.; dy = 0/72.
    # offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    # for label in ax1.xaxis.get_majorticklabels():
    #     label.set_transform(label.get_transform() + offset)

    ### FullLTO running time
    # ax4.set_title("Running time")
    # ax4.set_ylim(2000, 3600)
    # ax4.bar(['origin', 'dyncast_opt', 'sanitize', 'dyncast'], lto_runtime_tests, width, edgecolor='black', linewidth=1, color='tab:orange')
    # ax4.set_xticks(x, ['static_cast', 'dyncast_opt', 'sanitize', 'dyncast'], fontsize=fontsize)
    # ax4.set_yticklabels(['{0}'.format(round(x)) for x in ax1.get_yticks()], fontsize=fontsize)
    # ax4.set_ylabel('Macroseconds', fontsize=fontsize)
    # ax4.tick_params(axis='x', labelrotation=25)
    # plt.setp(ax1.xaxis.get_majorticklabels(), rotation=25, ha='right', rotation_mode='anchor', fontsize=17)

    ax2.set_title('Throughput')
    #ax2.set_ylim(360, 460)
    print(throughput_tests)
    print(lto_throughput_tests)
    print(throughput_tests)
    bars = []
    bar = ax2.bar(x, lto_throughput_tests, width, edgecolor=lto_edge_color, linewidth=1, color=lto_bar_color)
    bars.append(bar)
    bar = ax2.bar(x + width, throughput_tests, width, edgecolor=thin_edge_color, linewidth=1, color=thin_bar_color)
    ax2.set_xticks(x + width/2, labels, fontsize=fontsize)
    bars.append(bar)
    ax2.set_yticklabels(['{0}%'.format(round(x)) for x in ax2.get_yticks()], fontsize=fontsize)
    ax2.tick_params(axis='x', labelrotation=20)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=15, ha='right', rotation_mode='anchor', fontsize=17)

    ax3.set_title('Binary size')
    #ax3.set_ylim(1750, 1900)
    ax3.bar(x, lto_binary_size, width, edgecolor=lto_edge_color, linewidth=1, color=lto_bar_color)
    ax3.bar(x + width, binary_size, width, edgecolor=thin_edge_color, linewidth=1, color=thin_bar_color)
    ax3.set_xticks(x + width/2, labels, fontsize=fontsize)
    ax3.set_yticklabels(['{0}%'.format(round(x, 1)) for x in ax3.get_yticks()], fontsize=fontsize)
    #ax3.set_ylabel('MegaByte', fontsize=fontsize)
    ax3.tick_params(axis='x', labelrotation=20)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=15, ha='right', rotation_mode='anchor', fontsize=17)

    ax4.set_title('Peak Memory')
    #ax3.set_ylim(1750, 1900)
    ax4.bar(x, lto_memory_tests, width, edgecolor=lto_edge_color, linewidth=1, color=lto_bar_color)
    ax4.bar(x + width, memory_tests, width, edgecolor=thin_edge_color, linewidth=1, color=thin_bar_color)
    ax4.set_xticks(x + width/2, labels, fontsize=fontsize)
    ax4.set_yticklabels(['{0}%'.format(round(x, 1)) for x in ax4.get_yticks()], fontsize=fontsize)
    #ax3.set_ylabel('MegaByte', fontsize=fontsize)
    ax4.tick_params(axis='x', labelrotation=20)
    ax4.legend(bars, ['LTO', 'ThinLTO'], loc='lower right', ncols=1, fontsize='17', bbox_to_anchor=(2, 0.3))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=15, ha='right', rotation_mode='anchor', fontsize=17)
    plt.savefig("chrome.tocrop.pdf")
