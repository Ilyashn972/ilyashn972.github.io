
import os
import re
import subprocess

def get_image_sizes():
    """
    This function gets the pixel dimensions of all JPG images in the current directory and prints them.
    """
    try:
        result = subprocess.run(
            "sips -g pixelWidth -g pixelHeight *.jpg",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        # Process the output to print in a more readable format
        images = output.strip().split("\n/Users")
        for i, image_data in enumerate(images):
            if i == 0:
                image_data = image_data.strip()
            else:
                image_data = "/Users" + image_data.strip()
            
            if image_data:
                try:
                    lines = image_data.strip().split('\n')
                    image_path = lines[0]
                    width = re.search(r"pixelWidth: (\d+)", lines[1]).group(1)
                    height = re.search(r"pixelHeight: (\d+)", lines[2]).group(1)
                    print(f"{os.path.basename(image_path)}: {width}x{height}")
                except (IndexError, AttributeError) as e:
                    print(f"Could not parse data for an image: {image_data}, error: {e}")

    except FileNotFoundError:
        print("The 'sips' command is not available on this system.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing sips command: {e.stderr}")

if __name__ == "__main__":
    get_image_sizes()
