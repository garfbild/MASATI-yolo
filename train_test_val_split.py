import os
import random
import shutil
from pathlib import Path

def create_yolo_splits(image_dir, label_dir, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # Check if ratios sum to 1
    assert train_ratio + val_ratio + test_ratio == 1.0, "Ratios must sum to 1"
    
    # Get all image files (assuming they are .jpg/.png and labels are .txt)
    images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    
    # Shuffle images randomly
    random.shuffle(images)
    
    # Split the data
    num_images = len(images)
    train_split = int(train_ratio * num_images)
    val_split = int(val_ratio * num_images)
    
    train_images = images[:train_split]
    val_images = images[train_split:train_split + val_split]
    test_images = images[train_split + val_split:]

    # Define the paths for the output directories
    splits = {'train': train_images, 'val': val_images, 'test': test_images}
    
    for split, image_list in splits.items():
        # Create directories for images and labels
        image_output_dir = Path(output_dir) / split / 'images'
        label_output_dir = Path(output_dir) / split / 'labels'
        image_output_dir.mkdir(parents=True, exist_ok=True)
        label_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy images and their corresponding labels to the correct directories
        for image_name in image_list:
            image_path = Path(image_dir) / image_name
            label_path = Path(label_dir) / (image_name.replace(image_name.split('.')[-1], 'txt'))
            
            # Ensure the label file exists
            if not label_path.exists():
                print(f"Warning: Label file for {image_name} is missing!")
                continue
            
            # Copy image to the respective folder
            shutil.copy(image_path, image_output_dir)
            
            # Copy label to the respective folder
            shutil.copy(label_path, label_output_dir)

    print("Splitting complete!")

if __name__ == "__main__":
    os.chdir(f'C:\\DEV\\YOLO_BOLO\\MASATI-v2') # change this to point to your data

    image_dir = f'yolo_data\\images'  # Folder where your images are stored
    label_dir = f'yolo_data\\labels'  # Folder where your labels are stored
    output_dir = f'yolo_data\\output'  # Where you want to store the splits

    os.makedirs(output_dir, exist_ok=True)

    create_yolo_splits(image_dir, label_dir, output_dir)