import os

def get_shards_by_pool(pool_name):
    pool = pools.get(pool_name)
    print("pool", pool)
    if not pool:
        print(f"Pool {pool_name} not found.")
        return []

    shards = []
    for drive_type, path in pool.items():
        network_drives = get_network_drives()
        print("net", network_drives)
        drive_letter = next((drive[0] for drive in network_drives if drive[1] == path), None)
        if drive_letter:
            with os.scandir(drive_letter) as entries:
                for entry in entries:
                    folder_path = os.path.join(drive_letter, entry.name)
                    print("folder", folder_path)
                    if entry.is_dir():
                        outer_folder_size = get_outer_folder_size(folder_path) 
                        print("outer", outer_folder_size)
                        subfolder_sizes = get_subfolder_sizes(folder_path)
                        print("subfolders", subfolder_sizes)

                        if outer_folder_size is not None:
                            shards.append({
                                'pool': pool_name,
                                'type': drive_type,
                                'folder': entry.name,
                                'outer_folder_size': outer_folder_size,
                                'subfolder_sizes': subfolder_sizes,  # Add subfolder sizes here
                                'network_path': folder_path
                            })
                        print(shards)
    return shards


def get_outer_folder_size(folder_path):
    total_size = 0
    try:
        # Get the size of the outer folder itself (not subfolders)
        total_size += os.path.getsize(folder_path)
        print("outer folder", folder_path)

        with os.scandir(folder_path) as entries:
            for entry in entries:
                item_path = os.path.join(folder_path, entry.name)
                print("folder item", item_path)
                
                if entry.is_file():
                    file_size = os.path.getsize(item_path)
                    total_size += file_size
                    print(f"Size of {entry.name}: {file_size}, Total size: {total_size}")
                # Skip subfolders in this function to focus only on the outer folder
    except OSError as e:
        print(f"Error calculating folder size for {folder_path}: {e}")
        return None

    return total_size


def get_subfolder_sizes(folder_path):
    """Separate function to calculate the sizes of subfolders without affecting the outer folder size calculation."""
    subfolder_sizes = {}

    try:
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    subfolder_path = os.path.join(folder_path, entry.name)
                    folder_size = get_folder_size_recursive(subfolder_path)
                    subfolder_sizes[entry.name] = folder_size
                    print(f"Size of subfolder {entry.name}: {folder_size}")
    except OSError as e:
        print(f"Error calculating subfolder sizes for {folder_path}: {e}")
        return None

    return subfolder_sizes


def get_folder_size_recursive(folder_path):
    """Recursively calculate the size of a folder including its subfolders."""
    total_size = 0
    try:
        with os.scandir(folder_path) as entries:
            for entry in entries:
                item_path = os.path.join(folder_path, entry.name)
                if entry.is_file():
                    total_size += os.path.getsize(item_path)
                elif entry.is_dir():
                    total_size += get_folder_size_recursive(item_path)
    except OSError as e:
        print(f"Error calculating folder size for {folder_path}: {e}")
    return total_size
