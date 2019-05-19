from PIL import Image
import os
import sys
import skimage
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))

if __name__ == '__main__':
    folder_with_drones = sys.argv[1]
    folder_with_bgs = sys.argv[2]
    output_folder = sys.argv[3]

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    all_files = os.listdir(folder_with_drones)
    bg_files = os.listdir(folder_with_bgs)
    for d in all_files:
        drone = Image.open(os.path.join(folder_with_drones, d))
        #resize_factor = np.random.uniform(0.1,0.3,1)
        smaller_drone = drone.resize((int(drone.width * 0.3),int(drone.height * 0.3)))
        count = 0
        shuffle(bg_files)
        
        for b in bg_files[:20]:
            bg = Image.open(os.path.join(folder_with_bgs, b)).convert('RGBA')
            fitting_bg = bg.resize((smaller_drone.width, smaller_drone.height))

            new_img = Image.composite(smaller_drone, fitting_bg, smaller_drone)
            w,h = new_img.size
            random_pixel = int(np.random.uniform(0,20,1)[0])
            random_width = int(np.random.uniform(0,50,1)[0])
            new_img = new_img.crop((random_pixel,random_pixel,random_pixel + w-random_width,random_pixel + h*(w-random_width)/w))
            new_img_name = os.path.join(output_folder, '%s_%d.png' % (d[:-4], count))
            new_img_noise = skimage.util.random_noise(np.array(new_img.convert('RGB')),mode='gaussian',var=0.0001)
            Image.fromarray((new_img_noise*255).astype('uint8'),mode='RGB').save(new_img_name,'PNG')
        
            count = count + 1
            print('Saving image %s' % new_img_name)
