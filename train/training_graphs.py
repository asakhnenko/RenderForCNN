import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#Init variables
loss = []
iteration = []

loss_azimuth = []
loss_elevation = []
loss_tilt = []

acc_azimuth = []
acc_elevation = []
acc_tilt = []

def read_file(filename):
	f = open(filename,'r')
	for line in f:
		words_arr = line.split()
		if len(words_arr)>6:
			if words_arr[3].split(':')[0] == 'solver.cpp' and words_arr[4] == 'Iteration' and words_arr[-1] != '(#0)':
				if words_arr[5][-1] == ',':
					iteration.append((float)(words_arr[5][:-1]))
				else:
					iteration.append((float)(words_arr[5]))
				loss.append((float)(words_arr[-1]))
				tmp = f.readline().split()
				while tmp[3].split(':')[0] == 'data_layer.cpp' or tmp[4] == 'Iteration':
					#nothing
					tmp = f.readline().split()
				acc_azimuth.append((float)(tmp[-1]))
				f.readline()
				acc_elevation.append((float)(f.readline().split()[-1]))
				acc_tilt.append((float)(f.readline().split()[-1]))
				loss_azimuth.append((float)(f.readline().split()[-6]))
				loss_elevation.append((float)(f.readline().split()[-6]))
				loss_tilt.append((float)(f.readline().split()[-6]))

	f.close()

def read_file2(filename):
	f = open(filename,'r')
	last_iter = iteration[-1]
	for line in f:
		words_arr = line.split()
		if len(words_arr)>6:
			if words_arr[3].split(':')[0] == 'solver.cpp' and words_arr[4] == 'Iteration' and words_arr[-1] != '(#0)':
				if words_arr[5][-1] == ',':
					iteration.append((float)(words_arr[5][:-1])+last_iter)
				else:
					iteration.append((float)(words_arr[5])+last_iter)
				loss.append((float)(words_arr[-1]))
				tmp = f.readline().split()
				while tmp[3].split(':')[0] == 'data_layer.cpp' or tmp[4] == 'Iteration':
					#nothing
					tmp = f.readline().split()
				acc_azimuth.append((float)(tmp[-1]))
				f.readline()
				acc_elevation.append((float)(f.readline().split()[-1]))
				acc_tilt.append((float)(f.readline().split()[-1]))
				loss_azimuth.append((float)(f.readline().split()[-6]))
				loss_elevation.append((float)(f.readline().split()[-6]))
				loss_tilt.append((float)(f.readline().split()[-6]))

	f.close()

def mean_filter(arr, step):
	simplified_arr = []
	i = 0
	while i < len(arr):
		simplified_arr.append(np.mean(arr[i:i+step]))
		i += step
	return simplified_arr

read_file('drone_128_72bins_colored_lr014.e245428')

plt.title('Loss')
plt.plot(mean_filter(iteration,10),mean_filter(loss,10), lw=3, color='red')
plt.savefig('loss_both_big_scratch_cont.png')

f, axarr = plt.subplots(2, 1)
axarr[0].set_title('Accuracy')
axarr[0].plot(mean_filter(iteration,10),mean_filter(acc_azimuth,10), lw=2, color='blue')
axarr[0].plot(mean_filter(iteration,10),mean_filter(acc_elevation,10), lw=2, color='orange')
axarr[0].plot(mean_filter(iteration,10),mean_filter(acc_tilt,10), lw=2, color='green')
axarr[1].set_title('Loss')
axarr[1].plot(mean_filter(iteration,10),mean_filter(loss_azimuth,10), lw=2, color='blue')
axarr[1].plot(mean_filter(iteration,10),mean_filter(loss_elevation,10), lw=2, color='orange')
axarr[1].plot(mean_filter(iteration,10),mean_filter(loss_tilt,10), lw=2, color='green')
plt.setp(axarr[0].get_xticklabels(), visible=False)
plt.legend(handles=[mpatches.Patch(color='blue', label="Azimuth"),mpatches.Patch(color='orange', label="Elevation"),mpatches.Patch(color='green', label="Tilt")])
plt.savefig('separate_both_big_scratch_cont.png')
