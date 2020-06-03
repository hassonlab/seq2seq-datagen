import argparse
import glob
import os
import re
import time
from datetime import datetime

import numpy as np
from scipy.io import loadmat

from config import build_config
from utils import epoch_time, sort_nicely

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
print("Start Time: ", dt_string)
results_str = now.strftime("%Y-%m-%d-%H:%M")

parser = argparse.ArgumentParser()
parser.add_argument('--subjects', nargs='*', default=['625', '676'])
parser.add_argument('--electrodes', nargs='*', default=list(range(1, 65)))

args = parser.parse_args()
CONFIG = build_config(args, results_str)

start_time = time.time()

for subject_folder in CONFIG["CONV_DIRS"][1:]:
    print(f'Currently in: {subject_folder}')

    folder_split = subject_folder.split('/')
    folder_split.insert(-2, 'npy_data1')
    new_dir = '/'.join(folder_split)

    conv_list = glob.glob(os.path.join(subject_folder, 'NY*'))

    for conversation in conv_list:
        print(conversation)
        conv_split = conversation.split('/')

        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

        file_list = glob.glob(
            os.path.join(conversation, 'preprocessed', '*.mat'))
        file_list = sort_nicely(file_list)

        electrode_list = [
            int(re.search(r'file_(.*?).mat', file).group(1))
            for file in file_list
        ]

        first_conv = loadmat(file_list[0])['p1st']
        conv_length = first_conv.shape[0]

        data = np.zeros((conv_length, max(electrode_list)))
        data[:, 0] = np.squeeze(first_conv)

        # for conv in file_list[1:]:
        for electrode in electrode_list:
            my_str = os.path.join(conversation, 'preprocessed',
                                  '*' + str(electrode) + '.mat')
            elect_file = glob.glob(my_str)[0]
            insert_data = np.squeeze(loadmat(elect_file)['p1st'])
            loc = insert_data.size

            try:
                data[0:loc, electrode - 1] = insert_data
            except ValueError:
                print('+++++++++++++++++++++++++++++++++++++++++++++++++')
                temp = np.zeros((loc - conv_length, max(electrode_list)))
                conv_length = loc

                data = np.concatenate((data, temp), axis=0)
                data[0:loc, electrode - 1] = insert_data

        np.save(os.path.join(new_dir, conv_split[-1] + '.npy'), data)

end_time = time.time()

mins, secs = epoch_time(start_time, end_time)
print(f'Total time taken is: {mins} m {secs} s')
