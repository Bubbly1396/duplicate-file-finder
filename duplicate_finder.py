import os
import hashlib

def calculate_hash(file_path, chunk_size=4096):
    """
    this function calculates the hash value of a file.
    SHA-256 hashing is used to calculate hash.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
        return sha256.hexdigest()
    except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
            
def find_duplicates(folder_path):
    """
    this function finds the duplicate files in given folder.
    """
    files_by_size = {}
    duplicates = {}
    
    for root, _, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                size = os.path.getsize(file_path)
            except OSError:
                continue
                
            files_by_size.setdefault(size, []).append(file_path)
            
        for size, file_list in files_by_size.items():
            if len(file_list) < 2:
                continue
            
            hash_map = {}
            for file_path in file_list:
                file_hash = calculate_hash(file_path)
                if file_hash:
                    hash_map.setdefault(file_hash, []).append(file_path)
                    
            for file_hash, paths in hash_map.items():
                if len(paths) > 1:
                    duplicates[file_hash] = paths
        
        return duplicates
     
def remove_duplicates(duplicates, delete=False):
    """
    this function removes the duplicate copy of a file.
    keeps only original file.
    """
    for file_hash, files in duplicates.items():
        original = files[0]
        print(f"\nOriginal file kept : {original}")
        
    for dup in files[1:]:
        if delete:
            try:
                os.remove(dup)
                print(f"Deleted duplicatel: {dup}")
            except Exception as e:
                print(f"Failed to delete {dup}: {e}")
        else:
            print(f"Duplicate found: {dup}")
            

if __name__ == "__main__":
    folder = input("Enter folder path to scan: ")
    
    if not os.path.isdir(folder):
        print("Invalid folder path")
        exit()
        
    duplicates = find_duplicates(folder)
    
    if not duplicates:
        print("No duplicate files found")
    else:
        print(f"Duplicate groups found: {len(duplicates)}")
        choice = input("Do you want to delete duplicates? (yes/no): ").lower()
        remove_duplicates(duplicates, delete=(choice == "yes"))