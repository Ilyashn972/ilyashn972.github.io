
import subprocess
import os
import re

# Target dimensions for filtering
TARGET_WIDTH = 832
TARGET_HEIGHT = 1248

# The final dimensions after resizing
FINAL_WIDTH = 1184
FINAL_HEIGHT = 880

# Calculate the height for the initial crop to maintain the final aspect ratio.
# The width is kept at the original 832.
CROP_HEIGHT = int(TARGET_WIDTH / (FINAL_WIDTH / FINAL_HEIGHT))

def get_image_dimensions(filepath):
    """Gets the width and height of an image file using the 'sips' command."""
    try:
        cmd = f"sips -g pixelWidth -g pixelHeight '{filepath}'"
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.PIPE)
        width = int(re.search(r"pixelWidth: (\d+)", result).group(1))
        height = int(re.search(r"pixelHeight: (\d+)", result).group(1))
        return width, height
    except (subprocess.CalledProcessError, AttributeError, ValueError) as e:
        print(f"Could not get dimensions for {os.path.basename(filepath)}: {e}")
        return None, None

def process_images():
    """
    Finds images with 832x1248 dimensions, crops the middle, 
    and resizes them to 1184x880.
    """
    print(f"Searching for images with dimensions {TARGET_WIDTH}x{TARGET_HEIGHT}...")
    
    for filename in os.listdir('.'):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.abspath(filename)
            width, height = get_image_dimensions(filepath)

            if width == TARGET_WIDTH and height == TARGET_HEIGHT:
                print(f"Processing {filename}...")

                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_cropped{ext}"
                output_filepath = os.path.abspath(output_filename)

                # Step 1: Crop the center of the image to the calculated height and original width.
                # The 'sips -c' command crops to the given height and width from the center.
                crop_cmd = f"sips -c {CROP_HEIGHT} {TARGET_WIDTH} '{filepath}' --out '{output_filepath}'"
                try:
                    subprocess.run(crop_cmd, shell=True, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"  - Failed to crop {filename}. Error: {e.stderr.strip()}")
                    continue

                # Step 2: Resize the newly cropped image to the final dimensions.
                # The 'sips -z' command resizes the image to fit the given height and width.
                resize_cmd = f"sips -z {FINAL_HEIGHT} {FINAL_WIDTH} '{output_filepath}'"
                try:
                    subprocess.run(resize_cmd, shell=True, check=True, capture_output=True, text=True)
                    print(f"  - Successfully created {output_filename}")
                except subprocess.CalledProcessError as e:
                    print(f"  - Failed to resize {filename}. Error: {e.stderr.strip()}")
                    # Clean up the intermediate file if resize fails
                    if os.path.exists(output_filepath):
                        os.remove(output_filepath)

if __name__ == "__main__":
    process_images()
