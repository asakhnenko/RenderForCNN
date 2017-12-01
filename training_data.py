#!/usr/bin/python3
import os, csv
import global_variables

print('\n \nThis is a dataset generation script.\nPress Enter if you want to keep the same parameters as in previous iteration.\n\n')

csvfile = open('statistics.csv', 'r+')
data = list(csv.reader(csvfile))
last_data = data[-1]

dataset_id = int(last_data[0])+1

model_name = input('Enter the name of the 3D model : ')
if not model_name:
    model_name = last_data[1]
model = os.path.abspath(os.path.join(global_variables.g_model_folder, model_name + '.blend'))

views_amount = input('Enter the amount of views to be generated : ')
if not views_amount:
    views_amount = last_data[2]

azimuth_mean = input('Enter the azimuth mean : ')
if not azimuth_mean:
    azimuth_mean = last_data[3]

azimuth_std = input('Enter the azimuth standard deviation : ')
if not azimuth_std:
    azimuth_std = last_data[4]

elev_mean = input('Enter the elevation mean : ')
if not elev_mean:
    elev_mean = last_data[5]

elev_std = input('Enter the elevation standard deviation : ')
if not elev_std:
    elev_std = last_data[6]

tilt_mean = input('Enter the tilt mean : ')
if not tilt_mean:
    tilt_mean = last_data[7]

tilt_std = input('Enter the tilt standard deviation : ')
if not tilt_std:
    tilt_std = last_data[8]

bg_folder_name = input('Enter the background folder : ')
if not bg_folder_name:
    bg_folder_name = last_data[9]
    print()
bg_folder = os.path.abspath(os.path.join(global_variables.g_data_folder, bg_folder_name))
bg_amount = len(os.listdir(bg_folder))

dataset_name = 'drone_'+str(dataset_id)+'_'+views_amount+'_'+bg_folder_name
path_to_dataset= os.path.abspath(os.path.join(global_variables.g_datasets_folder, dataset_name))

writer = csv.writer(csvfile, delimiter=',')
writer.writerow([dataset_id,
                model_name,
                views_amount,
                azimuth_mean,
                azimuth_std,
                elev_mean,
                elev_std,
                tilt_mean,
                tilt_std,
                bg_folder_name,
                bg_amount,
                dataset_name])
csvfile.close()

print('\n\nSaving statistics to file\n\n')

print('\n\nCalling blender\n\n')

os.system("blender " + model + " --background --python render_pipeline/render_model_views.py " + views_amount +
            " " + azimuth_mean + " " + azimuth_std +
            " " + elev_mean + " " + elev_std +
            " " + tilt_mean + " " + tilt_std +
            " 1 2 " + path_to_dataset)

print('\n\nCreating LMDB dataset\n\n')

#subprocess.Popen(["python"path_to_dataset])
