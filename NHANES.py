# ---
# The NHANES data preprocessing
# ---

# modules
import numpy as np
import pandas as pd
from os.path import exists

# file location
path = './'

# part a. demographic dataset

# read data:
base_url = 'https://wwwn.cdc.gov/Nchs/Nhanes/'
cohorts = (
    ('2011-2012', 'G'),
    ('2013-2014', 'H'),
    ('2015-2016', 'I'),
    ('2017-2018', 'J')
    )

# new names for demo cols
demo_cols = {
    'SEQN': 'id',
    'RIDAGEYR': 'age',
    'RIDRETH3': 'race',
    'DMDEDUC2': 'education',
    'DMDMARTL': 'marital_status',
    'RIDSTATR': 'exam_status',
    'SDMVPSU': 'psu',
    'SDMVSTRA': 'strata',
    'WTMEC2YR': 'exam_wt',
    'WTINT2YR': 'interview_wt'
    }

# columns to convert to integer
demo_int = ['id', 'age', 'psu', 'strata']

# columns to convert to categorical
demo_cat = ['race', 'education', 
            'marital_status', 'exam_status']

# demographic data
demo_file = path + '/demo.feather'


if exists(demo_file):
    demo = pd.read_feather(demo_file)
else:
    demo_cohorts = []
    for cohort, label in cohorts:

        # read data and subset columns
        url = base_url + cohort + '/DEMO_' + label + '.XPT'
        dat = pd.read_sas(url)
        dat = dat[list(demo_cols.keys())]

        # assign cohort and collect
        dat['cohort'] = cohort
        demo_cohorts.append(dat)

    # concatenate and save
    demo = pd.concat(demo_cohorts, ignore_index=True)
    
    # rename columns
    demo = demo.rename(columns=demo_cols)
    
    # categorical variables
    for col in demo_cat:
        demo[col] = pd.Categorical(demo[col])
        
    demo['cohort'] = pd.Categorical(demo['cohort'])

    # integer variables
    for col in demo_int:
        demo[col] = pd.to_numeric(demo[col], downcast='integer')

    demo.to_feather(demo_file)


print(f"Demographic dataset finished. The shape is {demo.shape}")


# part b. ohx data

# new names for ohx cols
ohx_cols = {'SEQN': 'id',
            'OHDDESTS': 'dentition_status'}
tc_cols = {'OHX' + str(i).zfill(2) + 'TC':
           'tc_' + str(i).zfill(2) for i in range(1, 33)}
ctc_cols = {'OHX' + str(i).zfill(2) + 'CTC':
            'ctc_' + str(i).zfill(2) for i in range(2, 32)}
_, _ = ctc_cols.pop('OHX16CTC'), ctc_cols.pop('OHX17CTC')

ohx_cols.update(tc_cols)
ohx_cols.update(ctc_cols)

# columns to convert to integer
ohx_int = ['id']

# columns to convert to categorical
ohx_cat = ['dentition_status']

# dentition data
ohx_file = path + '/ohx.feather'

if exists(ohx_file):
    ohx = pd.read_feather(ohx_file)
else:
    ohx_cohorts = {}
    for cohort, label in cohorts:

        # read data and subset columns
        url = base_url + cohort + '/OHXDEN_' + label + '.XPT'
        dat = pd.read_sas(url).copy()
        dat = dat[list(ohx_cols.keys())].rename(columns=ohx_cols)

        # assign cohort and collect
        dat['cohort'] = cohort
        ohx_cohorts.update({cohort: dat})
 
    # concatenate
    ohx = pd.concat(ohx_cohorts, ignore_index=True)

    # categorical variables
    for col in ohx_cat:
        ohx[col] = pd.Categorical(ohx[col])
    
    for col in tc_cols.values():
        ohx[col] = pd.Categorical(ohx[col])

    # ctc columns get read in as bytes
    for col in ctc_cols.values():
        ohx[col] = ohx[col].apply(lambda x: x.decode('utf-8'))
        ohx[col] = pd.Categorical(ohx[col])

    ohx['cohort'] = pd.Categorical(ohx['cohort'])
    # integer variables
    for col in ohx_int:
        ohx[col] = pd.to_numeric(ohx[col], downcast='integer')

    # save
    ohx.to_feather(ohx_file)

print(f"Oral health and dentition dataset finished. The shape is {ohx.shape}")