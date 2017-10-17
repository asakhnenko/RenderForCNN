import Image
import os
import sys
import numpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))

if __name__ == '__main__':
    folder_with_drones = sys.argv[1]
    folder_with_bgs = sys.argv[2]
    output_folder = sys.argv[3]

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for d in os.listdir(folder_with_drones):
        drone = Image.open(os.path.join(folder_with_drones, d))
        for b in os.listdir(folder_with_bgs):
            bg = Image.open(os.path.join(folder_with_bgs, b)).convert('RGBA')
            new_img = Image.blend(bg, drone, 1)
            new_img_name = os.path.join(output_folder, '%s_%d.png' % (d[:-4], numpy.random.normal(0, 100, 1)[0]))
            new_img.convert('RGB').save(new_img_name, "PNG")
            print('Saving image %s' % new_img_name)
