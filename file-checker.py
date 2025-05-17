import os
import hashlib
import json

WATCHED_DIR = "./watched"
HASH_FILE = "file_hashes.json"

def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_all_file_hashes():
    hashes = {}
    for root, _, files in os.walk(WATCHED_DIR):
        for name in files:
            filepath = os.path.join(root, name)
            hashes[filepath] = hash_file(filepath)
    return hashes

def main():
    if not os.path.exists(HASH_FILE):
        print("Creating hash database...")
        with open(HASH_FILE, "w") as f:
            json.dump(get_all_file_hashes(), f, indent=4)
        print("Initial hash database created.")
    else:
        with open(HASH_FILE) as f:
            old_hashes = json.load(f)
        new_hashes = get_all_file_hashes()

        for path, hash_val in new_hashes.items():
            if path not in old_hashes:
                print(f"[NEW] {path}")
            elif old_hashes[path] != hash_val:
                print(f"[MODIFIED] {path}")

        for path in old_hashes:
            if path not in new_hashes:
                print(f"[DELETED] {path}")

if __name__ == "__main__":
    main()
