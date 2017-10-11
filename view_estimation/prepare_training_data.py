#!/usr/bin/python

'''
Prepare Training Data

Running this program will populate following folders:
  g_syn_images_lmdb_folder
    with img-label files and g_syn_images_lmdb_pathname_prefix+[_label,_image] LMDBs
  g_real_images_voc12train_all_gt_bbox_folder
    with cropped images and img-label files and g_real_images_voc12train_all_gt_bbox_lmdb_prefix+[_label,_image] LMDBs
'''

import os
import sys
import lmdb
from data_prep_helper import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
#from global_variables import *

if __name__ == '__main__':
    folder_with_img = sys.argv[1]
    folder_for_txt_files = sys.argv[2]
    txt_with_drone_types = sys.argv[3]

    # ----------------------------------
    # ---- SYNTHESIZED IMAGES ----------
    # ----------------------------------

    if not os.path.exists(folder_for_txt_files):
        os.mkdir(folder_for_txt_files)
    ##------------------------aly----------------------------
    # Separate generated images into two categories
    lines = [line.rstrip() for line in open(txt_with_drone_types, 'r')]
    drone_types = []

    for line in lines:
        ll = line.split(' ')
        drone_id = ll[0]
        drone_name = ll[1]
        drone_types.append(drone_name)
        get_one_category_image_label_file(folder_with_img,os.path.join(folder_for_txt_files, drone_name+'_train.txt'),
                                          os.path.join(folder_for_txt_files, drone_name+'_test.txt'))
    ##------------------------aly----------------------------
    for keyword in ['train', 'test']:
        input_file_list = [os.path.join(folder_for_txt_files, '%s_%s.txt' % (drone_type, keyword))
                           for drone_type in drone_types]
        output_file = os.path.join(folder_for_txt_files, 'all_%s.txt' % keyword)
        combine_files(input_file_list, output_file)
        
        # generate LMDB
        generate_image_view_lmdb(output_file, '%s_%s' % (output_file, keyword))
