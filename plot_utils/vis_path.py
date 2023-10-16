#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:45:51 2023

@author: gianvito
"""

import matplotlib.pyplot as plt
import imageio
from matplotlib.patches import Rectangle
import numpy as np
import os
import glob

def create_gif(exp_dir):
    
    sk_path = os.path.join(exp_dir, 'skill_history.txt')
    with open(sk_path) as f:
        lines = f.readlines()
    for idx, l in enumerate(lines):
        if 'Evaluation with agent scheduling = True' in l:
            start_idx = idx
            break
        
    path = []
    for l in lines[start_idx:]:
        if 'cppu' in l:
            path.append(l.split('\n')[0])
            
    run_id = exp_dir.split('/')[-1]
    print(f'{run_id} --> {path}')
    
    x = []
    y = []
    actions = []
    cppu_prev = ''
    
    for cppu_name in path:
        cppu_num = int(cppu_name.split('cppu')[-1])
        xy = cppu_num_to_xy(cppu_num)
        x.append(xy[0])
        y.append(xy[1])
        if cppu_name == cppu_prev:
            actions.append('skills')
        else:
            actions.append('transport')
        cppu_prev = cppu_name
        
    # print(actions) 
        
    time = np.arange(len(x))
    
    out_dir = os.path.join(exp_dir, 'gif')
    os.makedirs(out_dir, exist_ok=True)
    
    def create_frame(t):
        fig = plt.figure(figsize=(8, 6))
        plt.plot(x[:(t+1)], y[:(t+1)], color = 'grey' )
        plt.plot(x[t], y[t], color = 'black', marker = 'o' )
        plt.xlim([0,4])
        plt.ylim([0,4])
        
        plt.axis('off')
        ax = plt.gca()
        ax.add_patch(Rectangle((0.7, 0.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((1.7, 0.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((2.7, 0.8), 0.6, 0.4, alpha=0.2))
        
        ax.add_patch(Rectangle((0.7, 1.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((1.7, 1.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((2.7, 1.8), 0.6, 0.4, alpha=0.2))
        
        ax.add_patch(Rectangle((0.7, 2.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((1.7, 2.8), 0.6, 0.4, alpha=0.2))
        ax.add_patch(Rectangle((2.7, 2.8), 0.6, 0.4, alpha=0.2))
        
        if actions[t] == 'skills':
            ax.add_patch(Rectangle((x[t]-0.3, y[t]-0.2), 0.6, 0.4, alpha=0.3, color='orange'))
        
        plt.tight_layout()
        plt.savefig(f'{out_dir}/img_{t}.png', 
                    transparent = False,  
                    facecolor = 'white'
                   )
        plt.close()
    
    for t in time:
        create_frame(t)
        
    frames = []
    for t in time:
        image = imageio.v2.imread(f'{out_dir}/img_{t}.png')
        frames.append(image)
        
    imageio.mimsave(f'{out_dir}/path.gif', # output gif
                    frames,          # array of input frames
                    fps = 2)         # optional: frames per second
    
def cppu_num_to_xy(cppu_num):
    if cppu_num == 0:
        xy = [1,3]
    elif cppu_num == 1:
        xy = [2,3]
    elif cppu_num == 2:
        xy = [3,3]
    elif cppu_num == 4:
        xy = [1,2]
    elif cppu_num == 5:
        xy = [2,2]
    elif cppu_num == 6:
        xy = [3,2]
    elif cppu_num == 8:
        xy = [1,1]
    elif cppu_num == 9:
        xy = [2,1]
    elif cppu_num == 10:
        xy = [3,1]
    return xy
    
    
if __name__=='__main__':
    
    
    exp_dir = '/home/gianvito/Desktop/experiments/scenario_1/ppo_test/exp_1'
    
    list_results = glob.glob('{}/run_*/evaluation_info.json'.format(exp_dir))
    num_exp = len(list_results)

    for exp_id, res_path in enumerate(list_results):
        create_gif(os.path.dirname(res_path))
        
        
    
