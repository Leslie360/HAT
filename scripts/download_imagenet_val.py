
import os
from huggingface_hub import hf_hub_download

def download():
    save_dir = "data/imagenet"
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Downloading ImageNet-1K Validation Set to {save_dir}...")
    
    # We download the val.tar from a public ImageNet mirror on HF
    # Source: https://huggingface.co/datasets/imagenet-1k
    try:
        path = hf_hub_download(
            repo_id="imagenet-1k", 
            repo_type="dataset",
            filename="data/val_images.tar.gz", # Standard HF naming
            local_dir=save_dir,
            resume_download=True
        )
        print(f"Download complete: {path}")
    except Exception as e:
        print(f"HuggingFace download failed: {e}")
        print("Fallback: Attempting direct URL download...")
        # Direct link fallback (common Academic mirror)
        os.system(f"wget -c https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_val.tar -P {save_dir}")

if __name__ == "__main__":
    download()
