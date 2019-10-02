import os
import sys
sys.path.append('..')




fl_dir = r'D:\Data\Blocking\sample\fl'
nc_dir = r'D:\Data\Blocking\sample\nc'

def a():
    for file_name in os.listdir(fl_dir):
        if('res' in file_name):
            file_path = os.path.join(fl_dir, file_name)
            lines = None
            with open(file_path, 'r') as r_file:
                lines = r_file.readlines()
                
            
            lines = list(map(lambda x: str(x[0]) + '|' + x[1], enumerate(lines)))
            
            with open(file_path, 'w') as w_file:
                w_file.writelines(lines)
            
            
def change_filenames():
    for dir in [fl_dir, nc_dir]:
        for old_file_name in os.listdir(dir):
            if('res' in old_file_name or 'dup' in old_file_name or 'log' in old_file_name):
                old_file_path = os.path.join(dir, old_file_name)
                
                tokens = old_file_name.split('_')
                tokens.insert(-1, 't')
                
                new_file_name = '_'.join(tokens)
                new_file_path = os.path.join(dir, new_file_name)
                
                
                print(new_file_name)
                
                os.rename(old_file_path, new_file_path)
#                 
#                 
#                 os.rename(old_file_path, new)
#             


def count_records():
    fl_dir = r'D:\Data\Linkage\FL\FL16\data'
    nc_dir = r'D:\Data\Linkage\NC\NC16\data'
    
    for dir in [fl_dir, nc_dir]:
        
        line_cnt = 0
        
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            with open(filepath, 'r') as r_file:
                for line in r_file:
                    line_cnt += 1
        
        print(dir, line_cnt) 
                    
                
            
count_records()
