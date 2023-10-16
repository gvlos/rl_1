# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import glob
import scipy.stats as stats
import os
import matplotlib.colors as mcolors

def compute_90_int(res_arr, num_episodes):

    ci_low = []
    ci_high = []

    for eid in range(num_episodes):
        data = res_arr[:,eid]
        interval = stats.t.interval(confidence=0.9, df=len(data)-1,
                        loc=np.mean(data),
                        scale=stats.sem(data))
        ci_low.append(interval[0])
        ci_high.append(interval[1])

    return ci_low, ci_high


def read_data(exp_dir, metric, num_episodes):

    list_results = glob.glob('{}/run_*/evaluation_info.json'.format(exp_dir))
    num_exp = len(list_results)

    res_arr = np.zeros((num_exp, num_episodes))
    bt = [] # before training
    at = [] # after training

    for exp_id, res_path in enumerate(list_results):
        with open(res_path) as json_file:
            data = json.load(json_file)

        # product_names = data['training']['0'].keys()
        # print('Product names: {}'.format(product_names))
        product_names = ['Product0']

        res_dict = {}
        for product in product_names:
            res_dict[product] = []
            if data['training']:
                for eid in range(num_episodes):
                    ep_data = data['training'][str(eid)]
                    if product in ep_data.keys():
                        res_dict[product].append(ep_data[product][metric])
                    else:
                        res_dict[product].append(ep_data[metric])
            else:
                res_dict[product] = np.zeros(num_episodes)
            res_arr[exp_id, :] = res_dict[product]
            bt.append(data['before_training'][metric])
            at.append(data['after_training'][metric])

    return res_arr, bt, at

def plot_multiple(exp_dir, metric, num_run, param, param_label, mask=[]):
    
    list_experiments = sorted(glob.glob('{}/exp_*'.format(exp_dir)))
    
    labels = []
    y = []
    yerr = []
    baseline = []
    valid_run = []
    
    for folder in list_experiments:
        with open(os.path.join(folder, 'learning_config.json')) as config_file:
            learning_config = json.load(config_file)
        param_value = learning_config[param]
        num_episodes = learning_config["episodes"]
        
        if param_value not in mask:
            res_arr, bt, at = read_data(folder, metric, num_episodes)
            dm = np.mean(res_arr, axis=0)
            label = '{} = {}'.format(param_label, param_value)
            plt.plot(np.arange(num_episodes), dm, label=label)
            
            labels.append(label)
            y.append(np.mean(at))
            at_interval = stats.t.interval(confidence=0.9, df=len(at)-1,
                        loc=np.mean(at),
                        scale=stats.sem(at))
            yerr.append(np.mean(at)-at_interval[0])
            baseline += bt
            valid_run.append(res_arr.shape[0])
    
    plt.title('Training')
    plt.xlabel('episodes')
    plt.ylabel(metric)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(exp_dir, 'training.png'), dpi=200)
    plt.show()
    
    labels.append('baseline')
    y.append(np.mean(baseline))
    b_interval = stats.t.interval(confidence=0.9, df=len(baseline)-1,
                loc=np.mean(baseline),
                scale=stats.sem(baseline))
    yerr.append(np.mean(baseline) - b_interval[0])
    valid_run.append(num_run * len(list_experiments))
    
    interv = np.arange(5,5+len(labels))
    colors = list(mcolors.TABLEAU_COLORS.values())
    for x, y, yerr, vr in zip(interv, y, yerr, valid_run):
        if vr <= num_run:
            lab = '{}/{} run'.format(vr, num_run)
        else:
            lab = '{} run'.format(vr)
        plt.errorbar(x, y,
                     yerr= yerr, fmt='o', elinewidth=2, capsize=5,
                     color=colors[np.nonzero(np.unique(valid_run) == vr)[0][0]],
                     label=lab)
    plt.xticks(interv, labels, rotation = 70)
    plt.xlim([1,interv[-1]+4])
    plt.ylabel(metric)
    plt.title('Evaluation')
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.tight_layout()
    plt.savefig(os.path.join(exp_dir, 'evaluation.png'), dpi=200)
    plt.show()
            

def plot_two(exp_path_1, exp_path_2, metric, num_episodes, title, label_1, label_2):

    res_arr_1, bt_1, at_1 = read_data(exp_path_1, metric, num_episodes)
    ci_low_1, ci_high_1 = compute_90_int(res_arr_1, num_episodes)

    dm_1 = np.mean(res_arr_1, axis=0)

    at_interval_1 = stats.t.interval(confidence=0.9, df=len(at_1)-1,
                loc=np.mean(at_1),
                scale=stats.sem(at_1))

    res_arr_2, bt_2, at_2 = read_data(exp_path_2, metric, num_episodes)
    ci_low_2, ci_high_2 = compute_90_int(res_arr_2, num_episodes)

    dm_2 = np.mean(res_arr_2, axis=0)

    at_interval_2 = stats.t.interval(confidence=0.9, df=len(at_2)-1,
                loc=np.mean(at_2),
                scale=stats.sem(at_2))
    
    bt_avg = np.mean([bt_1[0], bt_2[0]])

    labels = ['BT', label_1, label_2]
    y = [bt_avg, np.mean(at_1), np.mean(at_2)]
    yerr = [0, np.mean(at_1)-at_interval_1[0], np.mean(at_2)-at_interval_2[0]]
    plt.errorbar(np.arange(5,8), y, yerr= yerr, fmt='o', elinewidth=2, capsize=5, color='green')
    plt.xticks(np.arange(5,8), labels)
    plt.xlim([1,11])
    plt.ylabel(metric)
    plt.title('Evaluation')
    plt.savefig('eval.png', dpi=200)

        
def plot_single(exp_dir, metric, num_episodes, title):

    res_arr, bt, at = read_data(exp_dir, metric, num_episodes)
    ci_low, ci_high = compute_90_int(res_arr, num_episodes)

    dm = np.mean(res_arr, axis=0)

    # at_interval = stats.t.interval(confidence=0.9, df=len(at)-1,
    #             loc=np.mean(at),
    #             scale=stats.sem(at))
    
    plt.plot(np.arange(num_episodes), dm)
    # plt.hlines(bt[0], 0, num_episodes-1, color='g', linestyles='--', label='Before training')
    # plt.hlines(np.mean(at), 0, num_episodes-1, color='orange', linestyles='--', label='After training')
    #plt.hlines(np.mean(dm), 0, num_episodes-1, color='b', linestyles='--', label='Average Training')
    plt.title(title)
    plt.xlabel('episodes')
    plt.ylabel(metric)
    plt.fill_between(np.arange(num_episodes), ci_low, ci_high, color='b', alpha=.15, label='.90% interval')
    # plt.fill_between(np.arange(num_episodes), at_interval[0], at_interval[1], color='orange', alpha=.15, label='.90% interval')
    plt.legend()
    plt.savefig(os.path.join(exp_dir, 'training_single.png'), dpi=200)
    


if __name__=='__main__':
    
    exp_dir = '/home/gianvito/Desktop/experiments/scenario_1/test_newmaster'
    metric = 'duration'
    num_episodes = 16
    title = 'd = 0.1'
    plot_single(exp_dir, metric, num_episodes, title)
    
    # exp_dir = '/home/gianvito/Desktop/experiments/scenario_2/best_replica'
    # metric = 'duration'
    # num_run = 5
    # param = 'epsilon'
    # # param = 'lr_decreasing_factor'
    # # param = 'clip_param'
    # param_label = 'eps'
    # mask = []
    # # res_arr, bt, at = read_data(exp_dir, metric, num_episodes)
    # plot_multiple(exp_dir, metric, num_run, param, param_label, mask)
