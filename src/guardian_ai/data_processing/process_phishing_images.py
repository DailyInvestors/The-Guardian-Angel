# src/guardian_ai/data_processing/process_phishing_images.py

import pandas as pd
from pathlib import Path
from tqdm import tqdm
from typing import Dict, Optional, List
from PIL import Image, UnidentifiedImageError

# --- Path Definitions ---
try:
    # This works when the script is run directly.
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
except NameError:
    # This provides a fallback for interactive environments.
    PROJECT_ROOT = Path('.').resolve()

RAW_IMAGES_DIR = PROJECT_ROOT / "data" / "raw" / "phishing_images"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

# --- Core Functions ---

def process_single_image(image_path: Path, label: str) -> Optional[Dict]:
    """
    Validates a single image file and extracts its metadata.

    Args:
        image_path: The path to the image file.
        label: The class label derived from the parent folder.

    Returns:
        A dictionary of metadata if the image is valid, otherwise None.
    """
    try:
        with Image.open(image_path) as img:
            # The .load() method forces Pillow to read the pixel data,
            # which is a robust way to check for file corruption.
            img.load()
            
            # Use relative paths for portability of the dataset
            relative_path = image_path.relative_to(PROJECT_ROOT).as_posix()
            
            return {
                'relative_path': relative_path,
                'label': label,
                'width': img.width,
                'height': img.height,
                'mode': img.mode, # e.g., 'RGB', 'RGBA', 'L' (grayscale)
                'is_valid': True
            }
    except UnidentifiedImageError:
        print(f"⚠️ Warning: Skipping non-image file: {image_path.name}")
        return None
    except Exception as e:
        print(f"⚠️ Warning: Corrupted or unreadable image '{image_path.name}'. Error: {e}")
        return None


def process_all_phishing_images():
    """
    Scans image directories, validates all images, and creates a
    metadata dataset file.
    """
    print("--- Starting Phishing Image Processing Pipeline ---")
    
    if not RAW_IMAGES_DIR.exists():
        raise FileNotFoundError(f"❌ Raw images directory not found at: {RAW_IMAGES_DIR}")

    # Get subdirectories, which represent our class labels
    labels = [d for d in RAW_IMAGES_DIR.iterdir() if d.is_dir()]
    if not labels:
        print("⚠️ Warning: No label subdirectories found in the raw images directory. Halting.")
        return

    print(f"✅ Found {len(labels)} class labels: {[l.name for l in labels]}")
    
    all_image_data = []
    
    for label_dir in labels:
        print(f"Processing label: '{label_dir.name}'...")
        # Create a list of all image files in the directory
        image_files: List[Path] = []
        for ext in SUPPORTED_EXTENSIONS:
            image_files.extend(label_dir.glob(f"*{ext}"))
        
        if not image_files:
            print(f"  - No images found for this label.")
            continue

        for image_path in tqdm(image_files, desc=f"  - Validating images"):
            metadata = process_single_image(image_path, label_dir.name)
            if metadata:
                all_image_data.append(metadata)

    if not all_image_data:
        print("❌ Error: No valid images were processed. Halting.")
        return
        
    print(f"\n✅ Successfully processed and validated {len(all_image_data)} images.")
    
    # Convert to DataFrame and save
    df = pd.DataFrame(all_image_data)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "processed_phishing_images_dataset.parquet"
    
    try:
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"🎉 Success! Image metadata dataset saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: Failed to save data to Parquet file. Reason: {e}")


if __name__ == "__main__":
    process_all_phishing_images()