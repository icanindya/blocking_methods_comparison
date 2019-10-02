# =============================================================================
# AUSTRALIAN NATIONAL UNIVERSITY OPEN SOURCE LICENSE (ANUOS LICENSE)
# VERSION 1.3
#
# The contents of this file are subject to the ANUOS License Version 1.2
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at:
#
#   http://datamining.anu.edu.au/linkage.html
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.
#
# The Original Software is: "deduplicate_multistep.py"
#
# The Initial Developers of the Original Software are:
#   Peter Christen
#
# Copyright (C) 2002 - 2011 the Australian National University and
# others. All Rights Reserved.
#
# Contributors:
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public License Version 2 or later (the "GPL"), in
# which case the provisions of the GPL are applicable instead of those
# above. The GPL is available at the following URL: http://www.gnu.org/
# If you wish to allow use of your version of this file only under the
# terms of the GPL, and not to allow others to use your version of this
# file under the terms of the ANUOS License, indicate your decision by
# deleting the provisions above and replace them with the notice and
# other provisions required by the GPL. If you do not delete the
# provisions above, a recipient may use your version of this file under
# the terms of any one of the ANUOS License or the GPL.
# =============================================================================

# =============================================================================
# Start of Febrl project module: "deduplicate_multistep.py"
#
# Generated using "guiFebrl.py" on Mon Apr 02 01:19:02 2018
# =============================================================================

# Import necessary modules (Python standard modules first, then Febrl modules)

import sys

sys.path.append('..')


import logging

import classification
import comparison
import dataset
import encode
import indexing
import measurements
import mymath
import output
import stringcmp
import time

import os

from fl_dataset import Record
import scipy.stats as sts
import numpy as np
import matplotlib.pyplot as plt 
import myutil
import fl_dataset as fl
import nc_dataset as nc



# -----------------------------------------------------------------------------
# Intialise a logger, set level to info oe warning

# log_level = logging.INFO # logging.WARNING
# my_logger = logging.getLogger()
# my_logger.setLevel(log_level)



# -----------------------------------------------------------------------------
# Febrl project type: Deduplicate
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

ds_size = 50000
duplicate_percentage = 30
methods = ['STD', 'SRT', 'QGM', 'CNP', 'STM', 'SFX']
missing_percentage_list = [10, 20]
corruption_percentage_list = [0, 5]


fl_ds_dir = r'D:\Data\Blocking\sample\fl'
nc_ds_dir = r'D:\Data\Blocking\sample\nc'


fl_field_list = [('index', 0),
                 ('first_name', 1),
                 ('middle_name', 2),
                 ('last_name', 3),
                 ('sex', 4),
                 ('race', 5),
                 ('birth_month', 6),
                 ('birth_day', 7),
                 ('birth_year', 8),
                 ('zip', 9),
                 ('county', 10),
                 ('party', 11),
                 ('reg_date', 12),
                 ('phone', 13),
                 ('voter_num', 14),
                 ('email', 15),
                 ('address', 16),
                 ('identifier', 17),
                 ('num_missing', 18),
                 ('num_corrupted', 19)]

nc_field_list = [('index', 0),
                 ('first_name', 1),  
                 ('middle_name', 2), 
                 ('last_name', 3),   
                 ('sex', 4),         
                 ('race', 5),        
                 ('ethnicity', 6),   
                 ('age', 7),         
                 ('birth_place', 8), 
                 ('zip', 9),         
                 ('county', 10),      
                 ('party', 11),      
                 ('reg_date', 12),   
                 ('phone', 13),      
                 ('voter_num', 14),  
                 ('nc_id', 15),      
                 ('address', 16),    
                 ('identifier', 17),
                 ('num_missing', 18),
                 ('num_corrupted', 19)]


fl_key_def_1 = [['last_name', 'last_name', False, False, None, [encode.get_substring, 0, 4]],
                ['birth_year', 'birth_year', False, False, None, [encode.get_substring, 2, 4]],
                ['sex', 'sex', False, False, None, []]]

fl_key_def_2 = [['first_name', 'first_name', False, False, None, [encode.get_substring, 0, 4]],
                ['middle_name', 'middle_name', False, False, None, [encode.get_substring, 0, 1]],
                ['birth_month', 'birth_month', False, False, None, []],
                ['birth_day', 'birth_day', False, False, None, []]]

fl_key_def_3 = fl_key_def_1 + fl_key_def_2

fl_keys_list = [[fl_key_def_1], [fl_key_def_2], [fl_key_def_3]]


nc_key_def_1 = [['last_name', 'last_name', False, False, None, [encode.dmetaphone, 4]],
                ['middle_name', 'middle_name', False, False, None, [encode.get_substring, 0, 1]],
                ['sex', 'sex', False, False, None, []],
                ['zip', 'zip', False, False, None, [encode.get_substring, 2, 5]]]

nc_key_def_2 = [['first_name', 'first_name', False, False, None, [encode.dmetaphone, 4]],
                ['age', 'age', False, False, None, []],
                ['address', 'address', False, False, None, [encode.dmetaphone, 4]]]

nc_key_def_3 = nc_key_def_1 + nc_key_def_2

nc_keys_list = [[nc_key_def_1], [nc_key_def_2], [nc_key_def_3]]


std_params_list = [[]]

srt_tight_params_list = [[2], [3], [5], [7], [10]]
srt_loose_params_list = [[100], [125], [150], [175], [200]] 

qgm_tight_params_list = [[2, 0.95], [2, 0.9], [3, 0.95], [3, 0.9]]
qgm_loose_params_list = [[2, 0.85], [2, 0.8], [3, 0.85], [3, 0.8]]

cnp_tight_params_list = [['jaccard', 'threshold', 0.9, 0.8, 2],
                         ['jaccard', 'threshold', 0.8, 0.7, 2],
                         ['jaccard', 'nearest', 5, 10, 2],
                         ['jaccard', 'nearest', 10, 20, 2],
                         ['tfidf', 'threshold', 0.9, 0.8, 2],
                         ['tfidf', 'threshold', 0.8, 0.7, 2],
                         ['tfidf', 'nearest', 5, 10, 2],
                         ['tfidf', 'nearest', 10, 20, 2]]
cnp_loose_params_list = [['jaccard', 'threshold', 0.6, 0.4, 2],
                         ['jaccard', 'threshold', 0.7, 0.5, 2],
                         ['jaccard', 'nearest', 50, 100, 2],
                         ['jaccard', 'nearest', 100, 200, 2],
                         ['tfidf', 'threshold', 0.6, 0.4, 2],
                         ['tfidf', 'threshold', 0.7, 0.5, 2],
                         ['tfidf', 'nearest', 50, 100, 2],
                         ['tfidf', 'nearest', 100, 200, 2]]
 
stm_tight_params_list = [[100, 20, 18, 'nearest', 20, 40],
                         [100, 20, 18, 'nearest', 50, 100],
                         [100, 20, 18, 'nearest', 10, 20]]

stm_loose_params_list = [[100, 20, 18, 'nearest', 20, 80],
                         [100, 20, 18, 'nearest', 50, 200],
                         [100, 20, 18, 'nearest', 10, 40]]
 
sfx_tight_params_list = [['allsubstr', 3, 5],
                         ['allsubstr', 3, 10],
                         ['allsubstr', 3, 15],
                         ['allsubstr', 5, 5],
                         ['allsubstr', 5, 10],
                         ['allsubstr', 5, 15],
                         ['suffixonly', 3, 5],
                         ['suffixonly', 3, 10],
                         ['suffixonly', 3, 15],
                         ['suffixonly', 5, 5],
                         ['suffixonly', 5, 10],
                         ['suffixonly', 5, 15]]
sfx_loose_params_list = [['allsubstr', 3, 100],
                         ['allsubstr', 4, 100],
                         ['allsubstr', 5, 100],
                         ['allsubstr', 3, 200],
                         ['allsubstr', 4, 200],
                         ['allsubstr', 5, 200],
                         ['suffixonly', 3, 100],
                         ['suffixonly', 4, 100],
                         ['suffixonly', 5, 100],
                         ['suffixonly', 3, 200],
                         ['suffixonly', 4, 200],
                         ['suffixonly', 5, 200]]
                         


def get_params_list(method_idx, keys_idx, is_tight):
    
    if method_idx == 0:
        return std_params_list
    
    elif method_idx == 1:
        if(is_tight):
            return srt_tight_params_list
        else:
            return srt_loose_params_list
        
    elif method_idx == 2:
        if(is_tight):
            return qgm_tight_params_list
        else:
            return qgm_loose_params_list
        
    elif method_idx == 3:
        if(is_tight):
            return cnp_tight_params_list
        else:
            return cnp_loose_params_list
        
    elif method_idx == 4:
        if(is_tight):
            return stm_tight_params_list
        else:
            return stm_loose_params_list
        
    elif method_idx == 5:
        if(is_tight):
            return sfx_tight_params_list
        else:
            return sfx_loose_params_list
    
def is_params_not_allowed(keys_idx, method_idx, is_tight, params_idx):
    
    if(keys_idx == 2 and method_idx == 2 and not is_tight):
        if params_idx in [1,2,3]:
            return True
        
    return False
        

def get_index_def(method_idx, keys, params, data_set_a, rec_comp):
    if method_idx == 0:
            
        index_def = indexing.DedupIndex(dataset1=data_set_a,
                                        dataset2=data_set_a,
                                        progress_report=10,
                                        rec_comparator=rec_comp,
                                        index_sep_str="",
                                        skip_missing=True,
                                        index_def=keys,
                                        block_method=("block", ))                       
            
    elif method_idx == 1:

        index_def = indexing.DedupIndex(dataset1=data_set_a,
                                        dataset2=data_set_a,
                                        progress_report=10,
                                        rec_comparator=rec_comp,
                                        index_sep_str="",
                                        skip_missing=True,
                                        index_def=keys,
                                        block_method=("sort", params[0]))

    elif method_idx == 2:

        index_def = indexing.DedupIndex(dataset1=data_set_a,
                                        dataset2=data_set_a,
                                        progress_report=10,
                                        rec_comparator=rec_comp,
                                        index_sep_str="",
                                        skip_missing=True,
                                        index_def=keys,
                                        block_method=("qgram", params[0], True, params[1]))

    elif method_idx == 3:

        index_def = indexing.CanopyIndex(dataset1=data_set_a,
                                         dataset2=data_set_a,
                                         progress_report=10,
                                         rec_comparator=rec_comp,
                                         index_sep_str="",
                                         skip_missing=True,
                                         index_def=keys,
                                         canopy_method=(params[0], params[1], params[2], params[3]),
                                         q=params[4],
                                         delete_perc=100,
                                         padded=True)

    elif method_idx == 4:

        index_def = indexing.StringMapIndex(dataset1=data_set_a,
                                            dataset2=data_set_a,
                                            progress_report=10,
                                            rec_comparator=rec_comp,
                                            index_sep_str="",
                                            skip_missing=True,
                                            index_def=keys,
                                            canopy_method=(params[3], params[4], params[5]),
                                            grid_resolution=params[0],
                                            dim=params[1],
                                            sub_dim=params[2],
                                            cache_dist=True,
                                            sim_funct=stringcmp.editdist)

    elif method_idx == 5:

        index_def = indexing.SuffixArrayIndex(dataset1 = data_set_a,
                                              dataset2 = data_set_a,
                                              progress_report = 10,
                                              rec_comparator = rec_comp,
                                              index_sep_str = "",
                                              skip_missing = True,
                                              index_def = keys,
                                              suffix_method = params[0],
                                              block_method = (params[1], params[2]),
                                              padded = True)
        
    return index_def    
    

def run():
    
    for ds in ['fl', 'nc']:
        if(ds == 'fl'):
            ds_dir = fl_ds_dir
            ds_keys_list = fl_keys_list
            ds_field_list = fl_field_list
        elif(ds == 'nc'):
            ds_dir = nc_ds_dir
            ds_keys_list = nc_keys_list
            ds_field_list = nc_field_list
        
        for corruption_percentage in corruption_percentage_list:
            
            for missing_percentage in missing_percentage_list:
                
                if(corruption_percentage == 5 and missing_percentage == 20):
                    continue
                            
                ds_path = os.path.join(ds_dir, '{}_missing_{}_corruption_{}.txt'.format(ds_size, missing_percentage, corruption_percentage))
                    
                # Define input data set A:
                #
                data_set_a = dataset.DataSetCSV(description="Data set",
                                                access_mode="read",
                                                strip_fields=True,
                                                miss_val=[''],
                                                rec_ident='r',
                                                file_name=ds_path,
                                                header_line=False,
                                                delimiter=",",
                                                field_list=ds_field_list)
        
                # -----------------------------------------------------------------------------
        
                # Define field comparison functions
                #
                fc_funct_1 = comparison.FieldComparatorExactString(agree_weight=1.0,
                                                                   description="Str-Exact-field-17-field-17",
                                                                   disagree_weight=0.0,
                                                                   missing_weight=0.0)
        
                field_comp_list = [(fc_funct_1, "identifier", "identifier")]
        
                rec_comp = comparison.RecordComparator(data_set_a, data_set_a, field_comp_list)
        
                # -----------------------------------------------------------------------------
            
                
                for keys_idx, keys in enumerate(ds_keys_list): 
                    
                    for method_idx, method in enumerate(methods):
                        
#                         if(method_idx == 4):
#                             continue
                        
                        for is_tight in [True, False]:
                        
                            result_file_path = myutil.get_result_path(ds_path, method, keys_idx, is_tight)
                            result_file = open(result_file_path, 'a')
                        
                            for params_idx, params in enumerate(get_params_list(method_idx, keys_idx, is_tight)):
                                
                                if(is_params_not_allowed(keys_idx, method_idx, is_tight, params_idx) or myutil.is_result_already_stored(result_file_path, params_idx)):
                                    continue
                                
                                
                                print(params)
                                
                                    
                                index_def = get_index_def(method_idx, keys, params, data_set_a, rec_comp)
                            
                                # init_logger
                                
                                for handler in logging.root.handlers[:]:
                                    logging.root.removeHandler(handler)
    
                                log_file_path = myutil.get_log_path(ds_path, method, keys_idx, is_tight, params_idx)
                                logging.basicConfig(filename=log_file_path,
                                                    filemode='w',
                                                    level=logging.INFO)
                                logging.getLogger()
                                
                                # ----------------------------------------------------------------------------
                                
                                
                                blocking_start_time = time.time()
                
                                # Build and compact index
                                index_def.build()
                                index_def.compact()
                                # Do record pair comparisons
                                [field_names_list, w_vec_dict] = index_def.run()
                                
                                blocking_end_time = time.time()
                                blocking_time = blocking_end_time - blocking_start_time
                            
                                # -----------------------------------------------------------------------------
                                                
                                comparison_start_time = time.time()
                            
                                # Define weight vector (record pair) classifier
                                classifier = classification.FellegiSunter(lower_threshold=0.99,
                                                                          upper_threshold=0.99)
                                # Unsupervised training of classifier
                                class_w_vec_dict = w_vec_dict  # Use orignal weight vector dictionary
                                classifier.train(class_w_vec_dict, set(), set())
                                # Classify all weight vectors
                                [m_set, nm_set, pm_set] = classifier.classify(class_w_vec_dict)
                
                                comparison_end_time = time.time()
                                comparison_time = comparison_end_time - comparison_start_time
                            
                                # -----------------------------------------------------------------------------
                            
                                # Define output file options
                                #
                                histo_str_list = output.GenerateHistogram(class_w_vec_dict, 1.0)
                                print(histo_str_list)
                                
                                match_count, recall, reduction_ratio, total_comparisons = myutil.get_metrics(ds_size, duplicate_percentage, histo_str_list)
                            
                                # for line in histo_str_list:
                                #     print line
                                match_file_path = myutil.get_matches_path(ds_path, method, keys_idx, is_tight, params_idx)
                                output.SaveMatchStatusFile(class_w_vec_dict, m_set, match_file_path)
                            
                                print('{} {} {}|{}, {:.2f}, {:.2f}, {}, {:.2f}, {:.2f}\n'.format(method, keys_idx, params_idx, match_count, recall, reduction_ratio, total_comparisons, blocking_time, comparison_time))
                                result_file.write('{}|{}, {:.2f}, {:.2f}, {}, {:.2f}, {:.2f}\n'.format(params_idx, match_count, recall, reduction_ratio, total_comparisons, blocking_time, comparison_time))
                                result_file.flush()
                            
if __name__ == '__main__':
    run()
            
# =============================================================================
# End of Febrl project module: "deduplicate_multistep.py"
# =============================================================================

# previous stm tight params
# [100, 20, 15, 'threshold', 0.8, 0.7],
# [1000, 20, 15, 'threshold', 0.8, 0.7]
