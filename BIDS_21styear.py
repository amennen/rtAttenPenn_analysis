#!/usr/bin/env python

# Script to convert and populate data in BIDS format
# Run with something like:
# ./code/BIDS_21st_year.py 

from os.path import exists, join
from os import makedirs
from glob import glob
from shutil import copyfile
import pandas as pd
import nibabel as nib
import json

# Set to True to actually copy files
copy_files = True

# Source of raw data on Princeton server
# Yaara's source directory:
# source_dir = '/mnt/bucket/labs/hasson/formerLabMembers/yaara/ABC/Raw'

# Claire's more recent source directory:
source_dir = '/scratch/claire/ABC/fMRI/Raw'

# Path to current BIDS directory
base_dir = '/jukebox/hasson/snastase/narratives'
bids_dir = join(base_dir, '21styear')
if not exists(bids_dir):
    makedirs(bids_dir)
    
# Set number of BOLD TRs to check
n_trs = 2249

# Original subject / session IDs and demographics
exclude = ['EW_030116', 'YA_030716']
df = pd.read_table(join(base_dir, 'subjects_spreadsheet.tsv'))
df = df.loc[df['Dataset'] == 'The 21st Year'][['Session', 'Age', 'Sex', 'Comprehension']]
df = df.loc[~df['Session'].isin(exclude)]

source_ids = df['Session'].tolist()
df = df.drop(labels='Session', axis=1)
rename = {'Age': 'age', 'Sex': 'sex', 'Comprehension': 'comprehension'}
df = df.rename(columns=rename)

bids_ids = ['sub-{0:03d}'.format(s) for s in range(1, len(source_ids) + 1)]
assert len(source_ids) == len(bids_ids)
df.insert(0, 'participant_id', bids_ids)

df.to_csv(join(bids_dir, 'participants.tsv'), sep='\t', index=False)

description_fn = join(bids_dir, 'dataset_description.json')
if exists(description_fn):
    description = {u'Funding': [u'TODO'], 
                   u'Name': u'The 21st Year',
                   u'License': u'PDDL (http://opendatacommons.org/licenses/pddl/)',
                   u'HowToAcknowledge': u'TODO',
                   u'Authors': [u'Yaara Yeshurun', 'Claire Chang', 'Yun-Fei Liu', 'Samuel A. Nastase', 'Uri Hasson'],
                   u'ReferencesAndLinks': [u'TODO'],
                   u'DatasetDOI': u'TODO',
                   u'BIDSVersion': u'1.1.0',
                   u'Acknowledgements': u'We thank the administrative staff of the Princeton Neuroscience Institute.'}
    with open(description_fn, 'w') as f:
        json.dump(description, f)

task_fn = join(bids_dir, 'task-21styear_bold.json')
if exists(task_fn):
    task = {'EchoTime': 0.028, 'RepetitionTime': 1.5, 
            'MagneticFieldStrength': 3, 'dcmmeta_slice_dim': 'TODO',
            'FlipAngle': 64, 'ProcedureStepDescription': 'The 21st Year',
            'CogAtlasID': 'passive listening',
            'PhaseEncodingDirection': 'j-', 'EffectiveEchoSpacing': 0,
            'dcmmeta_reorient_transform': [[0.0, -1.0, 0.0, 95.0],
            [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]], 
            'ManufacturersModelName': 'Skyra', 'dcmmeta_version': 0.6, 
            'dcmmeta_shape': [64, 64, 27, 2249], 'TaskName': '21styear',
            'ImageType': ['ORIGINAL', 'PRIMARY', 'FMRI', 'NONE', 'ND', 'NORM', 'MOSA'],
            'Manufacturer': 'Siemens'}
    with open(task_fn, 'w') as f:
        json.dump(task, f)

n_func, n_anat = [], []
for source_id, bids_id in zip(source_ids, bids_ids):
    if not exists(join(bids_dir, bids_id)):
        makedirs(join(bids_dir, bids_id))

    func_dir = join(bids_dir, bids_id, 'func')
    anat_dir = join(bids_dir, bids_id, 'anat')
    
    if not exists(func_dir):
        makedirs(func_dir)

    if not exists(anat_dir):
        makedirs(anat_dir)
        
    func_meta = {'EchoTime': 0.028, 'RepetitionTime': 1.5,
                 'MagneticFieldStrength': 3.0, 'PhaseEncodingDirection': 'j-',
                 'Manufacturer': 'Siemens', 'ManufacturersModelName': 'Skyra',
                 'FlipAngle': 64, 'TaskName': '21styear',
                 'SliceTiming': [0.0000, 0.7675, 0.0550, 0.8225, 0.1100, 0.8775,
                                 0.1650, 0.9325, 0.2200, 0.9875, 0.2750, 1.0425,
                                 0.3300, 1.0975, 0.3850, 1.1525, 0.4400, 1.2075,
                                 0.4950, 1.2625, 0.5500, 1.3175, 0.6050, 1.3725,
                                 0.6575, 1.4250, 0.7125],
                 'ParallelReductionFactorInPlane': 'TODO', 
                 'ParellelReductionType': 'TODO', 'EffectiveEchoSpacing': 0,
                 'PulseSequenceType': 'Gradient Echo EPI',                    
                 'NumberOfVolumesDiscardedByScanner': 4,                    
                 'InstitutionName': 'Princeton University',                    
                 'InstitutionAddress': 'Washington Rd, Building 25, Princeton, NJ 08540, USA',                    
                 'TaskDescription': 'Passively listened to audio story "The 21st Year"',
                 'CogAtlasID': 'https://www.cognitiveatlas.org/task/id/trm_4c8991fadfe01'}


    anat_meta = {'EchoTime': 0.003, 'RepetitionTime': 2.3,
                 'MagneticFieldStrength': 3,
                 'Manufacturer': 'Siemens', 'ManufacturersModelName': 'Skyra',
                 'FlipAngle': 'TODO'}
    
    func_fns = glob(join(source_dir, source_id, 'NII', '*epi*ABC.nii.gz'))
    func_keep = []
    for fn in func_fns:
        if nib.load(fn).shape[-1] == n_trs:
            func_keep.append(fn)
        else:
            print("Found EPI with wrong number of TRs--skipping it")
    assert len(func_keep) == 1
    func_in = func_fns[0]
    n_func.append(func_in)
    func_out = join(func_dir, bids_id + '_task-21styear_bold.nii.gz')
    func_json = join(func_dir, bids_id + '_task-21styear_bold.json')
    print("Copying {0}\n\tto {1}\n\twith {2}".format(
            func_in, func_out, func_json))
    if copy_files:
        copyfile(func_in, func_out)
        with open(func_json, 'w') as f:
            json.dump(func_meta, f)
    
    anat_fns = glob(join(source_dir, source_id, 'NII', 'o*mprage*.nii.gz'))
    assert len(anat_fns) == 1
    anat_in = anat_fns[0]
    n_anat.append(anat_in)
    anat_out = join(anat_dir, bids_id + '_T1w.nii.gz')
    anat_json = join(anat_dir, bids_id + '_T1w.json')
    print("Copying {0}\n\tto {1}\n\twith {2}".format(
            anat_in, anat_out, anat_json))
    
    if copy_files:
        copyfile(anat_in, anat_out)
        with open(anat_json, 'w') as f:
            json.dump(anat_meta, f)

assert len(bids_ids) == len(n_func) == len(n_anat)
print("Finished converting data to BIDS format")
