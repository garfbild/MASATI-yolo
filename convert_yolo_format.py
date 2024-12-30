import os
import pandas as pd
import xml.etree.ElementTree as ET
import shutil
import random
from pathlib import Path


def parse_annotation(root, verbose = 0):  
    folder = root.find('folder').text 
    filename = root.find('filename').text 
    path = root.find('path').text 
    
    source = root.find('source') 
    database = source.find('database').text 
    
    size = root.find('size') 
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    # for some reason a bunch have the wrong width/depth
    if width == 224:
        width = 512
    if height == 224:
        height = 512
    depth = size.find('depth').text 
    
    segmented = root.find('segmented').text 
    
    if verbose == 1:
        print(f"Folder: {folder}") 
        print(f"Filename: {filename}") 
        print(f"Path: {path}") # Extract source information 
        print(f"Database: {database}") # Extract size information 
        print(f"Width: {width}, Height: {height}, Depth: {depth}") # Extract segmented information 
        print(f"Segmented: {segmented}") # Extract object information 
    
    boats_array = [filename]
    for obj in root.findall('object'): 
        name = obj.find('name').text 
        pose = obj.find('pose').text 
        truncated = obj.find('truncated').text 
        difficult = obj.find('difficult').text 
        bndbox = obj.find('bndbox') 
        xmin = bndbox.find('xmin').text 
        ymin = bndbox.find('ymin').text 
        xmax = bndbox.find('xmax').text 
        ymax = bndbox.find('ymax').text
        if verbose == 1: 
            print(f"Object: {name}") 
            print(f" Pose: {pose}") 
            print(f" Truncated: {truncated}") 
            print(f" Difficult: {difficult}") 
            print(f" Bounding Box: ({xmin}, {ymin}), ({xmax}, {ymax})")

        xmin,xmax,ymin,ymax = int(xmin),int(xmax),int(ymin),int(ymax)

        center_x = ((xmin+xmax)/2)/width
        center_y = ((ymin+ymax)/2)/height

        bbox_width = (xmax-xmin)/width
        bbox_height = (ymax-ymin)/height

        boats_array.append([center_x,center_y,bbox_width,bbox_height])
    return boats_array

def prep_dataset(dataset):
    label_dir = f'{dataset}_labels'
    image_dir = f'{dataset}'

    yolo_label_dir = f'yolo_data\\labels'
    yolo_image_dir = f'yolo_data\\images'

    image_filenames = os.listdir(image_dir)

    if os.path.isdir(label_dir): # if images folder have an assocated labels folder
        label_filenames = os.listdir(label_dir)
        for label_filename, image_filename in zip(label_filenames, image_filenames):
            tree = ET.parse(os.path.join(label_dir, label_filename)) 
            root = tree.getroot()
            boats = parse_annotation(root)
            filename = f'{image_filename[:-4]}.txt'

            with open(os.path.join(yolo_label_dir, filename), 'w') as file: 
                for element in boats[1:]: 
                    file.write(f'0 {" ".join(map(str, element))} \n')

            src_file = os.path.join(image_dir,image_filename)
            dst_file = os.path.join(yolo_image_dir,image_filename)

            shutil.copy(src_file, dst_file)
    else:
        for image_filename in image_filenames:
            filename = f'{image_filename[:-4]}.txt'

            with open(os.path.join(yolo_label_dir, filename), 'w') as file: 
                file.write('')
            
            src_file = os.path.join(image_dir,image_filename)
            dst_file = os.path.join(yolo_image_dir,image_filename)

            shutil.copy(src_file, dst_file)
    print(f'completed {dataset}')

if __name__ == "__main__":
    os.chdir(f'C:\\DEV\\YOLO_BOLO\\MASATI-v2') # change this to point to your data
    print(os.listdir()) # should list out all subfolders coast, coast_ship ...

    os.makedirs(f'yolo_data', exist_ok=True)
    os.makedirs(f'yolo_data\\labels', exist_ok=True)
    os.makedirs(f'yolo_data\\images', exist_ok=True)

    prep_dataset("coast")
    prep_dataset("coast_ship")
    prep_dataset("multi")
    prep_dataset("ship")
    prep_dataset("water")
