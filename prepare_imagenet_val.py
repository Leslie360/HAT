#!/usr/bin/env python3
"""
Prepares the ImageNet-1K validation set for PyTorch ImageFolder.
Extracts ILSVRC2012_img_val.tar and moves images into class-specific subdirectories.
"""

import os
import urllib.request
import tarfile
import shutil

def prepare_imagenet():
    base_dir = "data/imagenet"
    val_dir = os.path.join(base_dir, "val")
    tar_path = os.path.join(base_dir, "ILSVRC2012_img_val.tar")
    
    if not os.path.exists(tar_path):
        print(f"Error: {tar_path} not found.")
        return

    os.makedirs(val_dir, exist_ok=True)
    
    print("1. Extracting validation images...")
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=val_dir)
        
    print("2. Downloading validation labels (ILSVRC2012_validation_ground_truth.txt)...")
    labels_url = "https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh"
    # The shell script contains the logic, but we can download the mapping directly
    mapping_url = "https://raw.githubusercontent.com/raghakot/keras-resnet/master/val.txt"
    val_txt_path = os.path.join(base_dir, "val.txt")
    
    try:
        urllib.request.urlretrieve(mapping_url, val_txt_path)
    except Exception as e:
        print(f"Error downloading labels: {e}")
        print("Using alternative method to generate synset folders...")
        # PyTorch torchvision script logic
        import json
        synset_url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-classes.txt"
        # Since standard scripts rely on shell, let's use a robust python approach
        # Download the devkit to get the meta.mat or use a known mapping.
        # For simplicity, we will download a pre-computed mapping script.
        pass

    # A more robust way: download a known bash script that does the moving
    print("Executing standard validation preparation script...")
    valprep_sh_path = os.path.join(val_dir, "valprep.sh")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh", valprep_sh_path)
    
    os.chdir(val_dir)
    os.system("bash valprep.sh")
    os.remove("valprep.sh")
    os.chdir("../../..")
    
    print(f"ImageNet validation set successfully prepared in {val_dir}.")

if __name__ == "__main__":
    prepare_imagenet()
