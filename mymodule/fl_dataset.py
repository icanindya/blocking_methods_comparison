import random
import os.path
import re
import numpy


orig_dir_path = 'D:/Data/Linkage/FL/FL16/data'
output_dir = r'D:\Data\Blocking\sample\fl'


#original file attribute indices
IN_IDX_COUNTY = 0
IN_IDX_VOTER_NUM = 1
IN_IDX_LAST_NAME = 2
IN_IDX_FIRST_NAME = 4
IN_IDX_MIDDLE_NAME = 5
IN_IDX_ADDRESS_LINE1 = 7
IN_IDX_ADDRESS_LINE2 = 8
IN_IDX_ADDRESS_CITY = 9
IN_IDX_ADDRESS_STATE = 10
IN_IDX_ZIP = 11
IN_IDX_SEX = 19
IN_IDX_RACE = 20
IN_IDX_BIRTH_DATE = 21
IN_IDX_REG_DATE = 22
IN_IDX_PARTY = 23
IN_IDX_PHONE_CODE = 34
IN_IDX_PHONE_NUM = 35
IN_IDX_EMAIL = 37

#generated file attribute indices
out_idx_first_name = 0
out_idx_middle_name = 1
out_idx_last_name = 2
out_idx_sex = 3
out_idx_race = 4
out_idx_birth_month = 5
out_idx_birth_day = 6
out_idx_birth_year = 7
out_idx_zip = 8
out_idx_county = 9
out_idx_party = 10
out_idx_reg_date = 11
out_idx_phone = 12
out_idx_voter_num = 13
out_idx_email = 14
out_idx_address = 15
out_idx_identifier = 16

blocking_indices = [out_idx_first_name,
                    out_idx_middle_name,
                    out_idx_last_name,
                    out_idx_sex,
                    out_idx_birth_month,
                    out_idx_birth_day,
                    out_idx_birth_year]

class Record:
    def __init__(self, first_name, middle_name, last_name, sex, race,
                  birth_month, birth_day, birth_year, zip, county, 
                  party, reg_date, phone, voter_num, email, address):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.race = race
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.birth_year = birth_year
        self.zip = zip
        self.county = county
        self.party = party
        self.reg_date = reg_date
        self.phone = phone
        self.voter_num = voter_num
        self.email = email
        self.address = address
        self.identifier = ''
    
    def __str__(self):
        return ','.join([self.first_name, self.middle_name, self.last_name, self.sex, self.race, 
                  self.birth_month, self.birth_day, self.birth_year, self.zip, self.county,
                   self.party, self.reg_date, self.phone, self.voter_num, self.email, self.address, self.identifier])
    
        


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
                    dob = tokens[IN_IDX_BIRTH_DATE]
                    dob_tokens = dob.split("/")
                    
                    birth_month = ''
                    birth_day = ''
                    birth_year = ''
                    
                    if(len(dob_tokens) == 3):
                        birth_month = dob_tokens[0]
                        birth_day = dob_tokens[1]
                        birth_year = dob_tokens[2]
                    
                    
                    zip = tokens[IN_IDX_ZIP]
                    county = tokens[IN_IDX_COUNTY]
                    party = tokens[IN_IDX_PARTY]
                    reg_date = tokens[IN_IDX_REG_DATE]
                    phone = tokens[IN_IDX_PHONE_CODE] + tokens[IN_IDX_PHONE_NUM]
                    voter_num = tokens[IN_IDX_VOTER_NUM]
                    email = tokens[IN_IDX_EMAIL]
            

                    address_template = tokens[IN_IDX_ADDRESS_LINE1] + ' ' + tokens[IN_IDX_ADDRESS_LINE2] + ' ' + tokens[IN_IDX_ADDRESS_CITY]
                    address = re.sub('\s+', ' ', address_template)
                    
                    
                    if(first_name and
                       last_name and
                       sex and
                       race and
                       birth_month and len(birth_month) == 2 and
                       birth_day and len(birth_day) == 2 and
                       birth_year and len(birth_year) == 4 and
                       zip and len(zip) == 5 and
                       county and
                       party and
                       reg_date and
                       phone and len(phone) == 10 and
                       voter_num and
                       email and
                       address
                       ):
                        record = Record(first_name, middle_name, last_name, sex, race, birth_month, birth_day, birth_year, zip, county, party, reg_date, phone, voter_num, email, address)
                        yield record 
                        

