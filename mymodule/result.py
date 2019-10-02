import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import deduplicate_dataset as ln
import myutil
from numpy.core.defchararray import startswith


metric_ylabel_dic = {'dr': 'Detection Rate',
                      'rr': 'Reduction Ratio',
                      'bt': 'Blocking Time (seconds)'}

metric_ylim_dic = {'dr': (0.0, 1.0),
                   'rr': (0.0, 1.0),
                   'bt': (0, 300)}

metric_token_idx_dic = {'dr': 0,
                        'rr': 3,
                        'bt': 4}

plot_dir = r'D:\Data\Blocking\plots'
plot_file_path = ''

def set_yticks(ax, min_val, max_val):
    
    lower_vals = list(np.arange(min_val, max_val, (max_val-min_val)/5.0))
    ytick_values = lower_vals + [max_val]
    
    ax.yaxis.set_ticks(ytick_values)

        
def set_yformat(ax, metric):
    if metric == 'dr':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        
    elif metric == 'rr':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        
    elif metric == 'bt':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    
        
def set_ylim(ax, metric):
    if(metric == 'dr'):
        ax.set_ylim([.60, 1.02])
        
    elif(metric == 'rr'):
        ax.set_ylim([0.972, 1.002])
    
    elif(metric == 'bt'):
        ax.set_ylim([-100, 2300])
    
        
def get_label(ds, key):
    if ds == 'fl':
        prefix = 'F' 
    elif ds == 'nc':
        prefix = 'N'
    
    if key < 3:
        return prefix + str(key+1) 
    else:
        return prefix + str(1) + '&' + prefix + str(2) 
    
    
def set_legend(ax, metric):
    if(metric == 'dr'):
        ax.legend(loc='lower right', bbox_to_anchor=(1.0,0.0), ncol=1, edgecolor='k',  fontsize='x-small')
    elif(metric == 'rr'):
        ax.legend(loc='lower left', bbox_to_anchor=(0.0,0.0), ncol=1, edgecolor='k',  fontsize='x-small')
    elif(metric == 'bt'):
        ax.legend(loc='upper right', bbox_to_anchor=(1.0,1.0), ncol=1, edgecolor='k',  fontsize='x-small')    


    

def plot(ds, all_key_met_mid_list, all_key_met_arm_list, metric, is_tight):
    
    mids = [item for sublist in all_key_met_mid_list for item in sublist]
    arms = [item for sublist in all_key_met_arm_list for item in sublist]
    
    max_val = max([mids[i] + arms[i] for i in range(len(mids))])
    min_val = min([mids[i] - arms[i] for i in range(len(mids))])
    
    marker_list = ['o', 'd', 's', 'h']
    sep = 4
    
    num_key = len(all_key_met_mid_list)
    num_method = len(all_key_met_mid_list[0])
    
    fig, ax = plt.subplots(figsize=(5.5, 3))
    
    x_start = 1
    
    for k in range(num_key):
    
        x = [x_start + i * (num_key + sep) + k for i in range(num_method)]
        y = all_key_met_mid_list[k]
        yerr = all_key_met_arm_list[k]

        ax.errorbar(x, y, yerr, label=get_label(ds, k), fmt='o', capsize=2, marker=marker_list[k], markeredgecolor='k', markersize=5)
        
    set_legend(ax, metric)


    set_ylim(ax, metric)
    
#     set_yticks(ax, min_val, max_val)
    
    plt.ylabel(metric_ylabel_dic[metric])
    xtick_positions = [x_start + i * (num_key + sep) + 1.5 for i in range(num_method) ]
    plt.xticks(xtick_positions, ln.methods)
    
    set_yformat(ax, metric)

#     plt.show()
    plt.savefig(plot_file_path, bbox_inches='tight')
    
    
def get_metric_val(ds_size, dup_percentage, metric, token_val):
    
    print(ds_size, dup_percentage, metric, token_val)
    
    num_actual_mat = (ds_size * dup_percentage)/100.0
    
    if(metric == 'dr'):
        return token_val/float(num_actual_mat)
        
    elif(metric == 'rr'):
        nc2 = (ds_size * (ds_size - 1))/2.0
        return 1.0 - (token_val/nc2)
        
    elif(metric == 'bt'):
        return token_val
    
    
def get_unique_matches_cnt(matches_file_path_list):
    
    smaller_id_set = set()
    
    for matches_file_path in matches_file_path_list:
        with open(matches_file_path, 'r') as r_file:
            for line in r_file:
                if not line.startswith('r'):
                    continue
                tokens = line.split(',')
                id1 = int(tokens[0][2:])
                id2 = int(tokens[1][2:])
                smaller_id = min([id1, id2])
                smaller_id_set.add(smaller_id)
                
    return len(smaller_id_set)


def get_key4_met_val(metric, ds_path, method, is_tight, params_idx):

    matches_file_path_list = []
    rr_relevant_token_val_list = []
    
    rr_met_val_list = []  
    bt_met_val_list = [] 
                                    
    for basic_keys_idx in [0, 1]:
        matches_file_path = myutil.get_matches_path(ds_path, method, basic_keys_idx, is_tight, params_idx)
        matches_file_path_list.append(matches_file_path)
        
        result_file_path = myutil.get_result_path(ds_path, method, basic_keys_idx, is_tight)
        with open(result_file_path, 'r') as r_file:
            for line in r_file:
                if(line.split('|')[0] != params_idx):
                    continue
                metrics_str = line.split('|')[1]
                tokens = list(map(lambda x: x.strip(), metrics_str.split(',')))
                
                rr_relevant_token_val = float(tokens[metric_token_idx_dic[metric]])
                rr_relevant_token_val_list.append(rr_relevant_token_val)
                
                bt_relevant_token_val = float(tokens[metric_token_idx_dic[metric]])
                bt_met_val = get_metric_val(ln.ds_size, ln.duplicate_percentage, metric, bt_relevant_token_val)
                bt_met_val_list.append(bt_met_val)
                
    if(metric == 'dr'):
        met_val = get_metric_val(ln.ds_size, ln.duplicate_percentage, metric, get_unique_matches_cnt(matches_file_path_list))
    
    elif(metric == 'rr'):
        met_val = get_metric_val(ln.ds_size, ln.duplicate_percentage, metric, sum(rr_relevant_token_val_list))
    
    elif(metric == 'bt'):
        met_val = get_metric_val(ln.ds_size, ln.duplicate_percentage, metric, sum(bt_met_val_list))
        
    return met_val

def set_plot_path(ds, ds_size, metric, missing_percentage, corruption_percentage, is_tight):
    global plot_file_path
    
    if is_tight:
        is_tight_str = 't'
    else:
        is_tight_str = 'l'
        
    plot_file_name = '{}_{}_{}_miss_{}_corr_{}_{}.pdf'.format(ds, ln.ds_size, metric, missing_percentage, corruption_percentage, is_tight_str) 
        
    plot_file_path = os.path.join(plot_dir, plot_file_name)
    

def run():
    
    for ds in ['fl', 'nc']:
        if(ds == 'fl'):
            ds_dir = ln.fl_ds_dir
            ds_keys_list = ln.fl_keys_list
            ds_field_list = ln.fl_field_list
        elif(ds == 'nc'):
            ds_dir = ln.nc_ds_dir
            ds_keys_list = ln.nc_keys_list
            ds_field_list = ln.nc_field_list
        
        for metric in ['dr', 'rr', 'bt']:
        
            for corruption_percentage in ln.corruption_percentage_list:
                
                for missing_percentage in ln.missing_percentage_list:
                    
                    if(corruption_percentage == 5 and missing_percentage == 20):
                        continue
                                
                    ds_path = os.path.join(ds_dir, '{}_missing_{}_corruption_{}.txt'.format(ln.ds_size, missing_percentage, corruption_percentage))
                    
                    for is_tight in [True, False]:
                    
                        all_key_metric_mid_list = []
                        all_key_metric_arm_list = []
                        
#                         print('len', len(ds_keys_list + [None]))
                        set_plot_path(ds, ln.ds_size, metric, missing_percentage, corruption_percentage, is_tight)
                        
                        for keys_idx, keys in enumerate(ds_keys_list + [None]): 
                            
                            key_metric_mid_list = []
                            key_metric_arm_list = []
                            
                            for method_idx, method in enumerate(ln.methods):
                                    
                                method_met_val_list = []
                                
                                if(keys_idx < 3):
                                    result_file_path = myutil.get_result_path(ds_path, method, keys_idx, is_tight)
                                    
                                    with open(result_file_path, 'r') as r_file:
                                        for line in r_file:
                                            metrics_str = line.split('|')[1]
                                            tokens = list(map(lambda x: x.strip(), metrics_str.split(',')))
                                            
                                            relevant_token_val = float(tokens[metric_token_idx_dic[metric]])
                                            met_val = get_metric_val(ln.ds_size, ln.duplicate_percentage, metric, relevant_token_val)
                                            method_met_val_list.append(met_val)
                                
                                else:
                                    result_file_path = myutil.get_result_path(ds_path, method, 0, is_tight)
                                    
                                    with open(result_file_path, 'r') as r_file:
                                        for line in r_file:
                                            params_idx = line.split('|')[0]
                                    
                                            met_val = get_key4_met_val(metric, ds_path, method, is_tight, params_idx)
                                            method_met_val_list.append(met_val)
                                            
                                    
                                method_met_val_max = max(method_met_val_list)
                                method_met_val_min = min(method_met_val_list)
                                method_met_val_mid = (method_met_val_max + method_met_val_min) / float(2)
                                method_met_val_arm = method_met_val_max - method_met_val_mid
                            
                                key_metric_mid_list.append(method_met_val_mid)
                                key_metric_arm_list.append(method_met_val_arm)
                                    
                                    
                            all_key_metric_mid_list.append(key_metric_mid_list)
                            all_key_metric_arm_list.append(key_metric_arm_list)
                        
                        plot(ds, all_key_metric_mid_list, all_key_metric_arm_list, metric, is_tight)   
                                    
                        
run()

