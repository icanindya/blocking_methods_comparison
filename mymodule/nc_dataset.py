import random
import os.path
import re
import numpy


orig_dir_path = r'D:\Data\Linkage\NC\NC16\data'
output_dir = r'D:\Data\Blocking\sample\nc'


#original file attribute indices
IN_IDX_COUNTY = 2
IN_IDX_VOTER_NUM = 3
IN_IDX_NC_ID = 4
IN_IDX_LAST_NAME = 11
IN_IDX_FIRST_NAME = 12
IN_IDX_MIDDLE_NAME = 13
IN_IDX_HOUSE_NUM = 15
IN_IDX_STREET_NAME = 18
IN_IDX_STREET_TYPE = 19
IN_IDX_CITY = 23
IN_IDX_STATE = 24
IN_IDX_ZIP = 25
IN_IDX_AREA_CODE = 33
IN_IDX_PHONE = 34
IN_IDX_RACE = 36
IN_IDX_ETHNICITY = 38
IN_IDX_PARTY = 39
IN_IDX_SEX = 41
IN_IDX_AGE = 43
IN_IDX_BIRTH_PLACE = 44
IN_IDX_REG_DATE = 45

#generated file attribute indices
out_idx_first_name = 0
out_idx_middle_name = 1
out_idx_last_name = 2
out_idx_sex = 3
out_idx_race = 4
out_idx_ethnicity = 5
out_idx_age = 6
out_idx_birth_place = 7
out_idx_zip = 8
out_idx_county = 9
out_idx_party = 10
out_idx_reg_date = 11
out_idx_phone = 12
out_idx_voter_num = 13
out_idx_nc_id = 14
out_idx_address = 15

blocking_indices = [out_idx_first_name,
                    out_idx_middle_name,
                    out_idx_last_name,
                    out_idx_sex,
                    out_idx_zip,
                    out_idx_age,
                    out_idx_address]

class Record:
    def __init__(self, first_name, middle_name, last_name, sex, race,
                  ethnicity, age, birth_place, zip, county, 
                  party, reg_date, phone, voter_num, nc_id, address):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.race = race
        self.ethnicity = ethnicity
        self.age = age
        self.birth_place = birth_place
        self.zip = zip
        self.county = county
        self.party = party
        self.reg_date = reg_date
        self.phone = phone
        self.voter_num = voter_num
        self.nc_id = nc_id
        self.address = address
        self.identifier = ''
    
    def __str__(self):
        return ','.join([self.first_name, self.middle_name, self.last_name, self.sex, self.race, 
                  self.ethnicity, self.age, self.birth_place, self.zip, self.county,
                   self.party, self.reg_date, self.phone, self.voter_num, self.nc_id, self.address, self.identifier])
    
        


def generate_records():
    
    for file_name in os.listdir(orig_dir_path):
        read_file_path = os.path.join(orig_dir_path, file_name)
        if(os.path.isfile(read_file_path)): 
            with open(read_file_path, 'r') as r_file:
                for line in r_file:
                    

                    
                    tokens = list(map(lambda x: x.strip(), line.split('\t')))
                    
                      
                    first_name = tokens[IN_IDX_FIRST_NAME].title()
                    middle_name = tokens[IN_IDX_MIDDLE_NAME].title()
                    last_name = tokens[IN_IDX_LAST_NAME].title()
                      
                    sex = ''
                    if(tokens[IN_IDX_SEX][:1].upper() == 'M'):
                        sex = 'M'
                    elif(tokens[IN_IDX_SEX][:1].upper() == 'F'):
                        sex = 'F'
                           
                    race = tokens[IN_IDX_RACE]
                    ethnicity = tokens[IN_IDX_ETHNICITY]
                    age = tokens[IN_IDX_AGE]
                    birth_place = tokens[IN_IDX_BIRTH_PLACE]
                      
                    zip = tokens[IN_IDX_ZIP]
                    county = tokens[IN_IDX_COUNTY]
                    party = tokens[IN_IDX_PARTY]
                    reg_date = tokens[IN_IDX_REG_DATE]
                    phone = tokens[IN_IDX_AREA_CODE] + tokens[IN_IDX_PHONE]
                    voter_num = tokens[IN_IDX_VOTER_NUM]
                    nc_id = tokens[IN_IDX_NC_ID]
              
  
                    address_template = tokens[IN_IDX_HOUSE_NUM] + ' ' + tokens[IN_IDX_STREET_NAME] + ' ' + tokens[IN_IDX_STREET_TYPE] + ' ' + tokens[IN_IDX_CITY]
                    address = re.sub('\s+', ' ', address_template)
                      
                    if(first_name and
                       last_name and
                       sex and
                       race and
                       ethnicity and
                       age and
                       birth_place and
                       zip and len(zip) == 5 and
                       county and
                       party and
                       reg_date and
                       phone and len(phone) == 10 and
                       voter_num and
                       nc_id and
                       address
                       ):
                        record = Record(first_name, middle_name, last_name, sex, race, ethnicity, age, birth_place, zip, county, party, reg_date, phone, voter_num, nc_id, address)
                        yield record 
                    