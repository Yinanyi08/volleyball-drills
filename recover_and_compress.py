import json
import os
from PIL import Image
import shutil

# Configuration
BACKUP_DIR = 'public_backup'
TARGET_DIR = 'public'
MAX_SIZE_MB = 1.8  # Leave some room for code
MAX_WIDTH = 800
QUALITY = 65

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def compress_images():
    print("Starting image compression...")
    ensure_dir(TARGET_DIR)
    
    total_size = 0
    compressed_count = 0
    
    # Copy directory structure first
    for root, dirs, files in os.walk(BACKUP_DIR):
        relative_path = os.path.relpath(root, BACKUP_DIR)
        target_root = os.path.join(TARGET_DIR, relative_path)
        ensure_dir(target_root)
        
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(target_root, file)
                
                try:
                    with Image.open(src_path) as img:
                        # Convert RGBA to RGB if needed (for saving as JPG to save more space, 
                        # but keeping PNG for transparency if strictly needed. 
                        # Let's stick to optimizing the current format or verifying size).
                        # For max compression, converting everything to JPG is best unless transparency exists.
                        
                        # Resize
                        if img.width > MAX_WIDTH:
                            ratio = MAX_WIDTH / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                        
                        # Save
                        # If it's PNG, we can try optimizing it or converting to JPG if no transparency
                        if file.lower().endswith('.png'):
                            # Check for transparency
                            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                                img.save(dest_path, optimize=True, quality=QUALITY)
                            else:
                                # Convert to JPG for size if no alpha
                                dest_path_jpg = os.path.splitext(dest_path)[0] + '.jpg'
                                img = img.convert('RGB')
                                img.save(dest_path_jpg, 'JPEG', quality=QUALITY)
                                # We might need to handle the extension change in the JS data later if we do this
                                # For safety now, let's KEEP extension but optimize
                                # RESETDEST
                                dest_path = os.path.join(target_root, file)
                                # Png doesn't use 'quality' param the same way in all libs, but let's try
                                img.save(dest_path, optimize=True) 
                        else:
                            img.save(dest_path, 'JPEG', quality=QUALITY)
                            
                    file_size = os.path.getsize(dest_path)
                    total_size += file_size
                    compressed_count += 1
                    
                except Exception as e:
                    print(f"Error processing {file}: {e}")
            else:
                # Copy non-image files directly
                src_path = os.path.join(root, file)
                dest_path = os.path.join(target_root, file)
                shutil.copy2(src_path, dest_path)
                total_size += os.path.getsize(dest_path)

    print(f"Compressed {compressed_count} images.")
    print(f"Total size of public folder: {total_size / 1024 / 1024:.2f} MB")
    
    if total_size > MAX_SIZE_MB * 1024 * 1024:
        print("WARNING: Still over the limit!")
    else:
        print("SUCCESS: Size is within limits.")

def revert_data_paths(file_path):
    print(f"Reverting paths in {file_path}...")
    if not os.path.exists(file_path):
        print("File not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple string replacement for the base URLs used previously
    # We need to be careful with JSON parsing to be robust
    import re
    
    # Regex to find http.../public/images/ and replace with /public/images/
    # Or just replace the specific domains we added
    
    content = content.replace("https://raw.githubusercontent.com/zyn1008/volleyball-drills/main/public", "/public")
    content = content.replace("https://cdn.jsdelivr.net/gh/zyn1008/volleyball-drills/public", "/public")
    
    # Also handle the jsDelivr specific conditioning path construction if it was hardcoded or generated
    # The previous script did: item['image'] = f"{CDN_BASE}/images/drills/{filename}"
    # We want: item['image'] = f"/public/images/drills/{filename}"
    
    # Let's do a robust JSON pass
    try:
        start = content.find('[')
        end = content.rfind(']') + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            data = json.loads(json_str)
            
            for item in data:
                img = item.get('image', '')
                if img.startswith('http'):
                    # Extract local path part
                    if '/images/' in img:
                        local_part = img.split('/images/')[-1]
                        # Reconstruct standard local path
                        # Check which category based on file path or content? 
                        # Easier: just look at the folder structure or preserve logical path
                        # logical path in public_backup is images/drills or images/conditioning
                        
                        # We need to know if it is drills or conditioning.
                        # drills.js usually points to drills, conditioning to conditioning.
                        # But let's check the file path passed to this function
                        subdir = 'drills'
                        if 'conditioning' in file_path:
                            subdir = 'conditioning'
                        elif 'drills' in img and 'conditioning' not in img:
                            subdir = 'drills'
                        elif 'conditioning' in img:
                            subdir = 'conditioning'
                            
                        # If the filename already contains the path
                        # fix_images.py set it to .../images/drills/filename
                        # so split by /images/ gives drills/filename or conditioning/filename
                        
                        new_path = '/public/images/' + local_part
                        item['image'] = new_path
            
            new_content = f"module.exports = {json.dumps(data, ensure_ascii=False, indent=2)};"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Paths reverted successfully.")
            
    except Exception as e:
        print(f"Error parsing JSON: {e}")

if __name__ == "__main__":
    # 1. Compress images from public_backup -> public
    compress_images()
    
    # 2. Revert JS data files to look at /public
    revert_data_paths('data/drills.js')
    revert_data_paths('data/conditioning.js')
