import json

def find_segment_holes(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: config file '{config_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{config_file}'.")
        return

    if "paragraphs" not in config or not isinstance(config["paragraphs"], list):
        print("Error: 'paragraphs' array not found or is not a list in config.json.")
        return

    all_segment_ids = set()
    for i, paragraph in enumerate(config["paragraphs"]):
        if "segment_ids" in paragraph and isinstance(paragraph["segment_ids"], list):
            for segment_id in paragraph["segment_ids"]:
                if isinstance(segment_id, int):
                    all_segment_ids.add(segment_id)
                else:
                    print(f"Warning: Non-integer segment_id found in paragraph at index {i}: {segment_id}")
        else:
            print(f"Warning: Paragraph at index {i} is missing 'segment_ids' list.")

    if not all_segment_ids:
        print("No segment_ids found in config.json.")
        return

    sorted_segment_ids = sorted(list(all_segment_ids))

    holes = []
    if sorted_segment_ids[0] > 1:
        for i in range(1, sorted_segment_ids[0]):
            holes.append(i)

    for i in range(len(sorted_segment_ids) - 1):
        current_id = sorted_segment_ids[i]
        next_id = sorted_segment_ids[i+1]
        if next_id - current_id > 1:
            for j in range(current_id + 1, next_id):
                holes.append(j)

    if holes:
        print("Holes found in segment_ids:")
        for hole in holes:
            print(f"- {hole}")
    else:
        print("No holes found in segment_ids.")

if __name__ == "__main__":
    find_segment_holes("config.json")