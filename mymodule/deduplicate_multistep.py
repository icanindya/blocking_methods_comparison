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


# -----------------------------------------------------------------------------
# Intialise a logger, set level to info oe warning
#
# log_level = logging.INFO # logging.WARNING
# my_logger = logging.getLogger()
# my_logger.setLevel(log_level)



# -----------------------------------------------------------------------------
# Febrl project type: Deduplicate
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------


ds_size_list = [50000]
index_method_dic = {1: 'standard', 2: 'sorting', 3: 'qgram', 4: 'canopy', 5: 'stringmap', 6: 'suffixarray'}
index_methods_chosen = [2]#[2, 6, 4, 1, 3, 5]
field_lists = ['list2', 'list_1', 'list3']
field_lists_chosen = ['list1', 'list2', 'list3']
corruption_levels = [0]#[0, 5, 10]
duplicate_percentage = 0.3

def index_and_classify(ds_size, corruption, index_def, index_method, field_list, param_index):

    # print '%s %s %d:\n' % (index_method_dic[index_method], field_list, param_index)

    # init_logger(ds_size, index_method, field_list, param_index)

    # Build and compact index
    #

    blocking_start_time = time.time()

    index_def.build()

    index_def.compact()

    # Do record pair comparisons
    #
    [field_names_list, w_vec_dict] = index_def.run()

    blocking_end_time = time.time()

    blocking_time = blocking_end_time - blocking_start_time

    # -----------------------------------------------------------------------------

    # Define weight vector (record pair) classifier
    #

    comparison_start_time = time.time()


    classifier = classification.FellegiSunter(lower_threshold=0.99,
                                              upper_threshold=0.99)

    # Unsupervised training of classifier
    #
    class_w_vec_dict = w_vec_dict  # Use orignal weight vector dictionary

    classifier.train(class_w_vec_dict, set(), set())

    # Classify all weight vectors
    #
    [m_set, nm_set, pm_set] = classifier.classify(class_w_vec_dict)

    comparison_end_time = time.time()

    comparison_time = comparison_end_time - comparison_start_time

    # -----------------------------------------------------------------------------

    # Define output file options
    #
    histo_str_list = output.GenerateHistogram(class_w_vec_dict, 1.0)


    # for line in histo_str_list:
    #     print line
    output.SaveMatchStatusFile(class_w_vec_dict, m_set,
                               "D:/Data/LinkageWithMissingValues/FL/FL16/sampled/results/dup_%d_%d_%s_%s_%d.txt" % (
                                ds_size_list[0], corruption, index_method_dic[index_method], field_list, param_index))

    print(histo_str_list)

    non_match_count = 0
    match_count = 0

    if len(histo_str_list) == 7:
        non_match_count = int(histo_str_list[4].split('|')[0].strip())
        match_count = int(histo_str_list[5].split('|')[0].strip())
    else:
        non_match_count = 0
        match_count = int(histo_str_list[4].split('|')[0].strip())
    recall = match_count / (ds_size * duplicate_percentage)
    total_comparisons = non_match_count + match_count
    reduction_ratio = (total_comparisons * 100)/((ds_size * (ds_size - 1))/2.0)


    print '%d, %.2f, %.2f, %d, %.2f, %.2f' % (match_count, recall, reduction_ratio, total_comparisons, blocking_time, comparison_time)
    all_result_file.write('%d, %.2f, %.2f, %d, %.2f, %.2f\n' % (match_count, recall, reduction_ratio, total_comparisons, blocking_time, comparison_time))

def init_logger(ds_size, index_method, field_list, param_index):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename="D:/Data/LinkageWithMissingValues/FL/FL16/sampled/results/log_%d_%s_%s_%d.txt" % (
    ds_size_list[0], index_method_dic[index_method], field_list, param_index),
                        filemode='w',
                        level=logging.INFO)
    logging.getLogger()



# Define indices for "blocking"
#

# last_name, sex, birth_year
index_def_1 = [["field-3", "field-3", False, False, None, []],
               ["field-4", "field-4", False, False, None, []],
               ["field-8", "field-8", False, False, None, []]]

# index_def_1 = [["field-4", "field-4", False, False, None, []],
#                ["field-8", "field-8", False, False, None, []],
#                ["field-3", "field-3", False, False, None, []]]

index_def_1 = [["field-3", "field-3", False, False, None, []],
               ["field-8", "field-8", False, False, None, []],
               ["field-4", "field-4", False, False, None, []]]


# birth_month, birth_day, first_name, middle_initial
# index_def_2 = [["field-6", "field-6", False, False, None, []],
#                ["field-7", "field-7", False, False, None, []],
#                ["field-1", "field-1", False, False, None, []],
#                ["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]]]

# index_def_2 = [["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]],
#                ["field-7", "field-7", False, False, None, []],
#                ["field-1", "field-1", False, False, None, []],
#                ["field-6", "field-6", False, False, None, []]]

index_def_2 = [["field-1", "field-1", False, False, None, []],
               ["field-7", "field-7", False, False, None, []],
                ["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]],
               
               ["field-6", "field-6", False, False, None, []]]

# last_name, sex, birth_year, birth_month, birth_day, first_name, middle_initial
# index_def_3 = [["field-3", "field-3", False, False, None, []],
#                ["field-4", "field-4", False, False, None, []],
#                ["field-8", "field-8", False, False, None, []],
#                ["field-6", "field-6", False, False, None, []],
#                ["field-7", "field-7", False, False, None, []],
#                ["field-1", "field-1", False, False, None, []],
#                ["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]]]


# index_def_3 = [["field-4", "field-4", False, False, None, []],
#                ["field-8", "field-8", False, False, None, []],
#                ["field-3", "field-3", False, False, None, []],
#                ["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]],
#                ["field-7", "field-7", False, False, None, []],
#                ["field-1", "field-1", False, False, None, []],
#                ["field-6", "field-6", False, False, None, []]]

index_def_3 = [
               ["field-3", "field-3", False, False, None, []],
               ["field-1", "field-1", False, False, None, []],
               ["field-8", "field-8", False, False, None, []],
               ["field-7", "field-7", False, False, None, []],
               ["field-2", "field-2", False, False, None, [encode.get_substring, 0, 1]],
               ["field-6", "field-6", False, False, None, []],
               ["field-4", "field-4", False, False, None, []]]

for ds_size in ds_size_list:
    all_result_file = open('D:/Data/LinkageWithMissingValues/FL/FL16/sampled/results/all_%d.txt' % ds_size, 'w')

    for corruption in corruption_levels:

        file_name_with_suffix = "D:/Data/LinkageWithMissingValues/FL/FL16/sampled/%d/part-00000-corrupted-%d" % (ds_size, corruption)

        print 'size = %d, corruption = %d:\n' % (ds_size, corruption)
        all_result_file.write('size = %d, corruption = %d:\n' % (ds_size, corruption))

        # Define input data set A:
        #
        data_set_a = dataset.DataSetCSV(description="Data set generated by Febrl GUI",
                                        access_mode="read",
                                        strip_fields=True,
                                        miss_val=[''],
                                        rec_ident='r',
                                        file_name=file_name_with_suffix,
                                        header_line=False,
                                        delimiter=",",
                                        field_list=[("field-0", 0),
                                                    ("field-1", 1),
                                                    ("field-2", 2),
                                                    ("field-3", 3),
                                                    ("field-4", 4),
                                                    ("field-5", 5),
                                                    ("field-6", 6),
                                                    ("field-7", 7),
                                                    ("field-8", 8),
                                                    ("field-9", 9),
                                                    ("field-10", 10),
                                                    ("field-11", 11),
                                                    ("field-12", 12),
                                                    ("field-13", 13),
                                                    ("field-14", 14),
                                                    ("field-15", 15),
                                                    ("field-16", 16),
                                                    ("field-17", 17)])

        # -----------------------------------------------------------------------------

        # Define field comparison functions
        #
        fc_funct_1 = comparison.FieldComparatorExactString(agree_weight=1.0,
                                                           description="Str-Exact-field-17-field-17",
                                                           disagree_weight=0.0,
                                                           missing_weight=0.0)

        field_comp_list = [(fc_funct_1, "field-17", "field-17")]

        rec_comp = comparison.RecordComparator(data_set_a, data_set_a, field_comp_list)

        # -----------------------------------------------------------------------------

        for field_list in field_lists_chosen:

            for index_method in index_methods_chosen:

                if field_list == 'list1':
                    index_def_list = [index_def_1]

                elif field_list == 'list2':
                    index_def_list = [index_def_2]

                elif field_list == 'list3':
                    index_def_list = [index_def_3]

                if index_method == 1:

                    print 'standard index with {}:\n'.format(field_list)
                    all_result_file.write('standard index with {}:\n'.format(field_list))

                    index_def = indexing.DedupIndex(dataset1=data_set_a,
                                                    dataset2=data_set_a,
                                                    progress_report=10,
                                                    rec_comparator=rec_comp,
                                                    index_sep_str="",
                                                    skip_missing=True,
                                                    index_def=index_def_list,
                                                    block_method=("block",))

                    index_and_classify(ds_size, corruption, index_def, index_method, field_list, 0)

                    all_result_file.flush()

                elif index_method == 2:

                    print 'sorting index with {}:\n'.format(field_list)
                    all_result_file.write('sorting index with {}:\n'.format(field_list))

                    param_set = [250]

                    if field_list == 'list1': param_set = [240]
                    elif field_list == 'list2': param_set = [250]
                    elif field_list == 'list3': param_set = [250]

                    for i in range(len(param_set)):

                        print 'param: %d\n' % (param_set[i])
                        all_result_file.write('param: %d\n' % (param_set[i]))

                        index_def = indexing.DedupIndex(dataset1=data_set_a,
                                                        dataset2=data_set_a,
                                                        progress_report=10,
                                                        rec_comparator=rec_comp,
                                                        index_sep_str="",
                                                        skip_missing=True,
                                                        index_def=index_def_list,
                                                        block_method=("sort", param_set[i]))

                        index_and_classify(ds_size, corruption, index_def, index_method, field_list, i)

                        all_result_file.flush()

                elif index_method == 3:

                    print 'q-gram index with {}:\n'.format(field_list)
                    all_result_file.write('q-gram index with {}:\n'.format(field_list))

                    param_set = [(2, 0.9)]

                    if field_list == 'list1': param_set = [(2, 0.90)]
                    elif field_list == 'list2': param_set = [(2, 0.90)]
                    elif field_list == 'list3': param_set = [(2, 0.95)]


                    for i in range(len(param_set)):

                        print 'param: {}\n'.format(param_set[i])
                        all_result_file.write('param: {}\n'.format(param_set[i]))

                        index_def = indexing.DedupIndex(dataset1=data_set_a,
                                                        dataset2=data_set_a,
                                                        progress_report=10,
                                                        rec_comparator=rec_comp,
                                                        index_sep_str="",
                                                        skip_missing=True,
                                                        index_def=index_def_list,
                                                        block_method=("qgram", param_set[i][0], True, param_set[i][1]))

                        index_and_classify(ds_size, corruption, index_def, index_method, field_list, i)

                        all_result_file.flush()

                elif index_method == 4:

                    print 'canopy index with {}:\n'.format(field_list)
                    all_result_file.write('canopy index with {}:\n'.format(field_list))

                    param_set = [('jaccard', 'threshold', .5, .32, 2)]

                    if field_list == 'list1': param_set = [('jaccard', 'threshold', 0.55, 0.35, 2)]
                    elif field_list == 'list2': param_set = [('jaccard', 'threshold', 0.5, 0.3, 2)]
                    elif field_list == 'list3': param_set = [('jaccard', 'threshold', 0.353, 0.25, 2)]

                    for i in range(len(param_set)):

                        print 'param: {}\n'.format(param_set[i])
                        all_result_file.write('param: {}\n'.format(param_set[i]))

                        index_def = indexing.CanopyIndex(dataset1=data_set_a,
                                                         dataset2=data_set_a,
                                                         progress_report=10,
                                                         rec_comparator=rec_comp,
                                                         index_sep_str="",
                                                         skip_missing=True,
                                                         index_def=index_def_list,
                                                         canopy_method=(param_set[i][0], param_set[i][1], param_set[i][2], param_set[i][3]),
                                                         q=param_set[i][4],
                                                         delete_perc=100,
                                                         padded=True)

                        index_and_classify(ds_size, corruption, index_def, index_method, field_list, i)

                        all_result_file.flush()

                elif index_method == 5:

                    print 'stringmap index with {}:\n'.format(field_list)
                    all_result_file.write('stringmap index with {}:\n'.format(field_list))

                    param_set = [(100, 20, 10)]

                    for i in range(len(param_set)):

                        print 'param: {}\n'.format(param_set[i])
                        all_result_file.write('param: {}\n'.format(param_set[i]))

                        index_def = indexing.StringMapIndex(dataset1=data_set_a,
                                                            dataset2=data_set_a,
                                                            progress_report=10,
                                                            rec_comparator=rec_comp,
                                                            index_sep_str="",
                                                            skip_missing=True,
                                                            index_def=index_def_list,
                                                            canopy_method=("threshold", .6, .4),
                                                            grid_resolution=param_set[i][0],
                                                            dim=param_set[i][1],
                                                            sub_dim=param_set[i][2],
                                                            cache_dist=True,
                                                            sim_funct=stringcmp.editdist)

                        index_and_classify(ds_size, corruption, index_def, index_method, field_list, i)

                        all_result_file.flush()

                elif index_method == 6:

                    print 'suffixarray index with {}:\n'.format(field_list)
                    all_result_file.write('suffixarray index with {}:\n'.format(field_list))

                    param_set = [('allsubstr', 4, 130)]

                    if field_list == 'list1': param_set = [('allsubstr', 6, 600)]
                    elif field_list == 'list2': param_set = [('allsubstr', 4, 800)]
                    elif field_list == 'list3': param_set = [('allsubstr', 4, 130)]

                    for i in range(len(param_set)):

                        print 'param: {}\n'.format(param_set[i])
                        all_result_file.write('param: {}\n'.format(param_set[i]))

                        index_def = indexing.SuffixArrayIndex(dataset1 = data_set_a,
                                                              dataset2 = data_set_a,
                                                              progress_report = 10,
                                                              rec_comparator = rec_comp,
                                                              index_sep_str = "",
                                                              skip_missing = True,
                                                              index_def = index_def_list,
                                                              suffix_method = param_set[i][0],
                                                              block_method = (param_set[i][1], param_set[i][2]),
                                                              padded = True)

                        index_and_classify(ds_size, corruption, index_def, index_method, field_list, i)

                        all_result_file.flush()

all_result_file.close()

# =============================================================================
# End of Febrl project module: "deduplicate_multistep.py"
# =============================================================================
