import os


def get_out_path(tag, ds_path, method, key_idx, is_tight, params_idx='x'):
    
    if(is_tight):
        is_tight_str = 't'
    else:
        is_tight_str = 'l'
    
    ds_dir_path, ds_file_name = os.path.split(ds_path)
    
    identifier =  '_{}_{}_{}_{}_{}'.format(tag, method.lower(), key_idx, is_tight_str, params_idx) 
    
    if '.' in ds_file_name:
        out_file_name = ds_file_name[:ds_file_name.rfind('.')] + identifier + ds_file_name[ds_file_name.rfind('.'):] 
        
    else:
        out_file_name = ds_file_name + identifier 
    
    out_path = os.path.join(ds_dir_path, out_file_name)
    
    return out_path

def get_result_path(ds_path, method, keys_idx, is_tight):
    
    return get_out_path('res', ds_path, method, keys_idx, is_tight)

def get_matches_path(ds_path, method, keys_idx, is_tight, params_idx):
    
    return get_out_path('dup', ds_path, method, keys_idx, is_tight, params_idx)

def get_log_path(ds_path, method, keys_idx, is_tight, params_idx):
    
    return get_out_path('log', ds_path, method, keys_idx, is_tight, params_idx)
    

def get_metrics(ds_size, duplicate_percentage, histo_str_list):
    
    non_match_count = 0
    match_count = 0

    if len(histo_str_list) == 7:
        non_match_count = int(histo_str_list[4].split('|')[0].strip())
        match_count = int(histo_str_list[5].split('|')[0].strip())
    else:
        non_match_count = 0
        match_count = int(histo_str_list[4].split('|')[0].strip())
    recall = match_count / float(ds_size * duplicate_percentage * 0.01)
    total_comparisons = non_match_count + match_count
    reduction_ratio = (total_comparisons * 100)/(float(ds_size * (ds_size - 1))/2)
    
    return match_count, recall, reduction_ratio, total_comparisons


def is_result_already_stored(result_file_path, params_idx):
    with open(result_file_path, 'r') as r_file:
        for line in r_file:
            if line.startswith(str(params_idx) + '|'):
                 return True
    return False
    