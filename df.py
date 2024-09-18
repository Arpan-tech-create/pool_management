import subprocess
import psutil
import re
import os
import shutil
# Dictionary to store master and slave paths
pools = {
    'pool1': {
        'master': '\\\\192.168.2.64\\data18',
        'slave': '\\\\192.168.2.65\\data18'
    },
    'pool2': {
        'master': '\\\\192.168.2.64\\data16',
        'slave': '\\\\192.168.2.65\\data16'
    }
}

def get_network_drives():
    network_drives = []
    try:
        command = "net use"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = result.stdout

        drive_pattern = re.compile(r'([A-Z]:)\s+\\\\([^\s]+)')
        valid_ips = ['192.168.2.64', '192.168.2.65']
        for line in output.splitlines():
            match = drive_pattern.search(line)
            if match:
                drive_letter = match.group(1)
                network_path = f"\\\\{match.group(2)}"
                ip_address = network_path.split('\\')[2]
                if any(ip_address.startswith(ip) for ip in valid_ips):
                    network_drives.append((drive_letter, network_path))
    except Exception as e:
        print(f"Error fetching network drives: {e}")
    
    return network_drives

def get_drive_space_info(drive_letter):
    try:
        usage = psutil.disk_usage(drive_letter)
        total_space = usage.total / (1024**3)  # Convert bytes to GB
        free_space = usage.free / (1024**3)    # Convert bytes to GB
        return round(total_space, 2), round(free_space, 2)
    except Exception as e:
        print(f"Error retrieving space info for {drive_letter}: {e}")
        return None, None
    

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
            for folder in os.listdir(drive_letter):
                folder_path = os.path.join(drive_letter, folder)
                print("folder",folder_path)
                if os.path.isdir(folder_path):
    
                    outer_folder_size = get_outer_folder_size(folder_path)
                    print("outer",outer_folder_size)

                   
                    total_capacity, used_space, free_space = get_disk_usage(folder_path)

                    if outer_folder_size is not None and total_capacity is not None and free_space is not None:
                        occupied_space = total_capacity - free_space
                        shards.append({
                            'pool': pool_name,
                            'type': drive_type,
                            'folder': folder,
                            'total_capacity': total_capacity,
                            'free_space': free_space,
                            'occupied_space': occupied_space,
                            'outer_folder_size': outer_folder_size,
                            'network_path': folder_path
                        })
                    print(shards)
    return shards

def get_outer_folder_size(folder_path):
    """Calculates the size of the outer folder and its immediate contents."""
    total_size = 0
    try:
      
        total_size += os.path.getsize(folder_path)
        print("TPTTT",folder_path)

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            print("item",item_path)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)

                print(f"Size of {item}: {total_size}")

    except OSError as e:
        print(f"Error calculating folder size for {folder_path}: {e}")
        return None

    return total_size

def get_disk_usage(folder_path):
    """Returns the total capacity, used space, and free space of the drive containing folder_path."""
    try:
        total, used, free = shutil.disk_usage(folder_path)
        print(f"Disk usage for {folder_path} - Total: {total}, Used: {used}, Free: {free}")
        return total, used, free
    except OSError as e:
        print(f"Error getting disk usage for {folder_path}: {e}")
        return None, None, None