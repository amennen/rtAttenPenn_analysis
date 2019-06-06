#!/usr/bin/env python

# Run from ~/storyteller/scripts with something like
# ./story_glm.py 01 fsaverage6 |& tee ../data/derivatives/logs/story_glm_sub-01_fsaverage6_log.txt &
# ./story_glm.py 01 MNI152NLin2009cAsym |& tee ../data/derivatives/logs/story_glm_sub-01_MNI152_log.txt &

from sys import argv
from os import chdir, makedirs
from os.path import exists, join
from subprocess import call
import numpy as np

subject = argv[1]
space = argv[2]
sessions = {'bronx': 374, 'pieman': 277}
spaces = ['T1w', 'MNI152NLin2009cAsym', 'fsaverage6']
assert space in spaces

base_dir = '/usr/people/snastase/storyteller/data/'
scripts_dir = join(base_dir, 'code')
func_dir = join(base_dir, 'sub-'+subject, 'func')
fmri_dir = join(base_dir, 'derivatives')

# Convert fmriprep's confounds.tsv for 3dDeconvolve -ortvec per run
for session, n_vol in sessions.items():

    prep_dir = join(fmri_dir, 'fmriprep', 'sub-'+subject, 'ses-'+session, 'func')
    glm_dir = join(fmri_dir, 'afni', 'sub-'+subject, 'ses-'+session, 'func')
    reg_dir = join(glm_dir, 'regressors')
    if not exists(reg_dir):
        makedirs(reg_dir)

    with open(join(prep_dir,
                   'sub-{0}_ses-{1}_task-speak_bold_confounds.tsv'.format(
                    subject, session))) as f:
        lines = [line.strip().split('\t') for line in f.readlines()]

    confounds = {}
    for confound_i, confound in enumerate(lines[0]):
        confound_ts = []
        for tr in lines[1:]:
            confound_ts.append(tr[confound_i])
        confounds[confound] = confound_ts

    keep = ['FramewiseDisplacement', 'aCompCor00', 'aCompCor01', 'aCompCor02',
            'aCompCor03', 'aCompCor04', 'X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']
    ortvec = {c: confounds[c] for c in keep}

    # Create de-meaned and first derivatives of head motion (backward difference with leading zero)
    for motion_reg in ['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']:
        motion = [float(m) for m in ortvec[motion_reg]]
        motion_demean = np.array(motion) - np.mean(motion)
        motion_deriv = np.insert(np.diff(motion_demean, n=1), 0, 0)
        assert len(motion_demean) == len(motion_deriv) == len(ortvec[motion_reg])
        ortvec[motion_reg + '_demean'] = ['{:.9f}'.format(m) for m in motion_demean]
        ortvec[motion_reg + '_deriv'] = ['{:.9f}'.format(m) for m in motion_deriv]
        del ortvec[motion_reg]

    assert len(ortvec) == 18

    with open(join(reg_dir, 'sub-{0}_ses-{1}_task-speak_bold_ortvec.1D'.format(subject, session)), 'w') as f:
        rows = []
        for tr in range(len(ortvec['FramewiseDisplacement'])):
            row = []
            for confound in ortvec:
                if ortvec[confound][tr] == 'n/a':
                    row.append('0')
                else:
                    row.append(ortvec[confound][tr])
            assert len(row) == 18
            row = '\t'.join(row)
            rows.append(row)
        assert len(rows) == n_vol
        f.write('\n'.join(rows))

    # Change directory for AFNI
    chdir(glm_dir)

    if space == 'fsaverage6':
        # Run AFNI's 3dTproject
        # HaxbyLab filter "-passband 0.00667 0.1", Hasson Lab "-stopband 0 0.00714"
        for side, hemi in [('L', 'lh'), ('R', 'rh')]:
            cmd = ("3dTproject -polort 2 -stopband 0 0.00714 -TR 1.5 -input " 
                        "{0}/sub-{1}_ses-{2}_task-speak_bold_space-fsaverage6.{3}.func.gii "
                        "-ort {4} "
                        "-prefix {5}/sub-{1}_ses-{2}_task-speak.{6}.tproject.gii".format(
                            prep_dir, subject, session, side,
                            join(reg_dir, 'sub-{0}_ses-{1}_task-speak_bold_ortvec.1D'.format(subject, session)),
                            glm_dir, hemi))
            print("Regressing out confounds using AFNI's 3dTproject"
                  "\tSubject {0}, {1}, {2} hemisphere".format(subject, session, hemi))
            call(cmd, shell=True)
            print("\tFinished regressing out confounds!")
    elif space != 'fsaverage6':
        # Run AFNI's 3dTproject
        cmd = ("3dTproject -polort 2 -stopband 0 0.00714 -TR 1.5 -input " 
                    "{0}/sub-{1}_ses-{2}_task-speak_bold_space-{3}_preproc.nii.gz "
                    "-ort {4} -mask {0}/sub-{1}_ses-{2}_task-speak_bold_space-{3}_brainmask.nii.gz "
                    "-prefix {5}/sub-{1}_ses-{2}_task-speak.{3}.tproject.nii.gz".format(
                        prep_dir, subject, session, space,
                        join(reg_dir, 'sub-{0}_ses-{1}_task-speak_bold_ortvec.1D'.format(subject, session)),
                        glm_dir))
        print("Regressing out confounds using AFNI's 3dTproject"
              "\tSubject {0}, {1}".format(subject, session))
        call(cmd, shell=True)
        print("\tFinished regressing out confounds!")
