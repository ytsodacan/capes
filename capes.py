import os
import json
import uuid

def generate_marketplace_json():
    # Define directory paths
    capes_dir = 'capes'
    output_file = 'marketplace.json'
    
    # Supported image formats
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    # Check if the capes folder exists
    if not os.path.exists(capes_dir):
        print(f"Error: The folder '{capes_dir}' does not exist.")
        print("Please create a folder named 'capes' and put your cape textures inside it.")
        return

    # Gather all files in the capes directory
    files = os.listdir(capes_dir)
    
    # Filter out anything that isn't a valid image file
    image_files = [f for f in files if f.lower().endswith(valid_extensions)]
    
    # Separate main textures from thumbnails to avoid duplicates
    # This looks for files ending in "_thumb" or "_thumbnail"
    texture_files = []
    thumbnail_files = {}

    for f in image_files:
        name_without_ext, ext = os.path.splitext(f)
        
        if name_without_ext.lower().endswith(('_thumb', '_thumbnail')):
            # It's a thumbnail. Strip the suffix to find its "base name" key
            base_name = name_without_ext.lower().replace('_thumbnail', '').replace('_thumb', '')
            thumbnail_files[base_name] = f"{capes_dir}/{f}"
        else:
            texture_files.append(f)

    marketplace_data = []

    for f in texture_files:
        filename, ext = os.path.splitext(f)
        
        # Clean up the filename to make a clean, readable display name
        # e.g., "fire_cape_128x" -> "Fire Cape 128x"
        clean_name = filename.replace('_', ' ').replace('-', ' ').title()
        
        # Create a unique database ID safe for HTML selectors
        safe_id = filename.replace(' ', '_').replace('-', '_').lower()
        
        # Check if this texture has a corresponding thumbnail file
        thumb_path = thumbnail_files.get(safe_id, "")
        
        # Construct the item entry matching your layout
        cape_entry = {
            "id": safe_id,
            "name": clean_name,
            "texture": f"{capes_dir}/{f}",
            "thumbnail": thumb_path
        }
        
        marketplace_data.append(cape_entry)
        print(f"Added: {clean_name} (Thumbnail: {'Yes' if thumb_path else 'No, falling back to texture'})")

    # Write the clean data array to your marketplace.json file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(marketplace_data, json_file, indent=4)
        
    print(f"\nSuccess! Successfully mapped {len(marketplace_data)} capes into '{output_file}'.")

if __name__ == "__main__":
    generate_marketplace_json()