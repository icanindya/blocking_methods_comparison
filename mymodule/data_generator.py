import random
import os
import numpy

import fl_dataset as fl
import nc_dataset as nc

ds = fl

size = 50000
duplicate_percentage = 30


def run(ds, scale):
    
    missing1_percentage = 5 * scale
    missing2_percentage = 3 * scale
    missing3_percentage = 2 * scale
    missing_percentage = missing1_percentage + missing2_percentage + missing3_percentage

    missing1_prob = missing1_percentage/100.0
    missing2_prob = missing2_percentage/100.0
    missing3_prob = missing3_percentage/100.0
    missing_prob = missing_percentage/100.0                    
    probs = [1.0 - missing_prob, missing1_prob, missing2_prob, missing3_prob]
    
    num_original_record = int((size * (100 - duplicate_percentage))/100)
        
    original_record_list = random.sample(list(ds.generate_records()), num_original_record)
    enumerated_original_record_list = []
       
    for identifier, record in enumerate(original_record_list):
        record.identifier = str(identifier)
        enumerated_original_record_list.append(record)
        
    num_duplicates = int((size * duplicate_percentage)/100)
    
    enumerated_duplicate_record_list = random.sample(enumerated_original_record_list, num_duplicates)
    
    combined_record_list = enumerated_original_record_list + enumerated_duplicate_record_list
    
    output_file_path = os.path.join(ds.output_dir, '{}_missing_{}_corruption_0.txt'.format(size, missing_percentage))
    
    with open(output_file_path, 'w') as w_file:
        for index, record in enumerate(combined_record_list):
            
            record_tokens = str(record).split(',')
    
            num_missing = numpy.random.choice(numpy.arange(len(probs)), p=probs)
            
            print(num_missing)
            
            missing_indices = []
                
            while(len(missing_indices) < num_missing):
                chosen_idx = random.choice(ds.blocking_indices)
                if(not chosen_idx in missing_indices):
                    missing_indices.append(chosen_idx)
                    record_tokens[chosen_idx] = ''
                
            
            all_tokens = [str(index)] + record_tokens + [str(num_missing) + ',0\n'] 
            line = ','.join(all_tokens)
            w_file.write(line)  
        
if __name__ == '__main__':
    for ds in [fl, nc]:
        for scale in [1, 2]:
            run(ds, scale)