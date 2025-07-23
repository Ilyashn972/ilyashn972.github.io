import os
import json
from together import Together
from PIL import Image
import requests
from io import BytesIO

# Initialize the Together AI client
client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

# Load the configuration file
try:
    with open('multimedia/config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: multimedia/config.json not found.")
    exit()

def find_paragraph(search_line):
    """Finds a paragraph in the config that contains the search_line."""
    for i, paragraph in enumerate(config['paragraphs']):
        paragraph_text = ' '.join(paragraph['lines'])
        if search_line.lower() in paragraph_text.lower():
            return i, paragraph
    return None, None

def main():
    """Main function to run the interactive image editing process."""
    while True:
        # Get the source paragraph for the base image
        try:
            source_search_input = input("Enter a line from the paragraph for the base image (or 'quit' to exit): ")
        except EOFError:
            print("\nExiting.")
            break

        if source_search_input.lower() == 'quit':
            break

        if not source_search_input.strip():
            print("Please enter some text.")
            continue

        _, source_paragraph = find_paragraph(source_search_input)

        if source_paragraph is None:
            print(f"Could not find a source paragraph containing the line: '{source_search_input}'")
            continue

        print("\nFound source paragraph:")
        print(f"  {' '.join(source_paragraph['lines'])}")
        
        image_path = source_paragraph.get('image')
        if not image_path:
            print("Source paragraph has no associated image.")
            continue

        # Get the target paragraph to place the new image
        try:
            target_search_input = input("Enter a line from the paragraph to place the new image (or 'quit' to exit): ")
        except EOFError:
            print("\nExiting.")
            break

        if target_search_input.lower() == 'quit':
            break

        if not target_search_input.strip():
            print("Please enter some text.")
            continue

        target_paragraph_index, target_paragraph = find_paragraph(target_search_input)

        if target_paragraph is None:
            print(f"Could not find a target paragraph containing the line: '{target_search_input}'")
            continue
            
        print("\nFound target paragraph:")
        print(f"  {' '.join(target_paragraph['lines'])}")

        # Display the current image
        try:
            full_local_path = os.path.join('multimedia', image_path)
            print(f"Displaying current image: {full_local_path}")
            img = Image.open(full_local_path)
            img.show()
        except FileNotFoundError:
            print(f"Could not find image file: {full_local_path}")
            continue

        # Get a new prompt from the user
        new_prompt = input("Enter a new prompt for the image (or 'skip' to cancel): ")

        if new_prompt.lower() == 'skip':
            continue
        
        # This script assumes images are publicly accessible via a URL for the API.
        # This base URL is based on the previous script's logic.
        # You may need to adjust this if your image hosting changes.
        base_image_url = "https://ilyashn972.github.io/7e71ecbb7830fd69dc78ba1369a452129b88e980fdbb6d63285fbb8f912f/costa/multimedia/"
        full_image_url = f"{base_image_url}{image_path}"
        
        print(f"Using image URL for generation: {full_image_url}")

        # Generation and confirmation loop
        while True:
            try:
                print("Generating new image (this may take a moment)...")
                image_completion = client.images.generate(
                    model="black-forest-labs/FLUX.1-kontext-pro",
                    width=1024,
                    height=768,
                    prompt=new_prompt,
                    image_url=full_image_url
                )
                new_image_url = image_completion.data[0].url
                
                # TODO save the new image to /tmp folder and print the name
                
                print("Displaying new image...")
                response = requests.get(new_image_url)
                response.raise_for_status()
                new_img = Image.open(BytesIO(response.content))
                new_img.show()

                accept = input("Accept this image? (yes/no/retry): ").lower()
                if accept == 'yes':
                    # Create new filenames using the target paragraph's info
                    segment_id = target_paragraph['segment_ids'][0]
                    new_image_filename = f"costa_{segment_id:03d}_edited.jpg"
                    new_prompt_filename = f"costa_{segment_id:03d}_edited.prompt.txt"
                    
                    new_image_rel_path = os.path.join("images", new_image_filename)
                    new_prompt_rel_path = os.path.join("images", new_prompt_filename)

                    new_image_abs_path = os.path.join("multimedia", new_image_rel_path)
                    new_prompt_abs_path = os.path.join("multimedia", new_prompt_rel_path)

                    # Save the new image and prompt
                    os.makedirs(os.path.dirname(new_image_abs_path), exist_ok=True)
                    new_img.save(new_image_abs_path)
                    with open(new_prompt_abs_path, 'w') as f:
                        f.write(new_prompt)

                    # Update the config object for the target paragraph
                    config['paragraphs'][target_paragraph_index]['image'] = new_image_rel_path
                    config['paragraphs'][target_paragraph_index]['prompt'] = new_prompt_rel_path
                    
                    # Write the updated config back to the file
                    with open('multimedia/config.json', 'w') as f:
                        json.dump(config, f, indent=4)
                    
                    print(f"Updated config with new image: {new_image_rel_path}")
                    break 
                elif accept == 'no':
                    print("Discarding new image.")
                    break
                elif accept == 'retry':
                    print("Retrying generation...")
                    continue
                else:
                    print("Invalid input. Please enter 'yes', 'no', or 'retry'.")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading new image: {e}")
                break
            except Exception as e:
                print(f"An error occurred during image generation: {e}")
                break
    
    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
