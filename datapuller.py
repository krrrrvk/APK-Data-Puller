import argparse
import adbutils
import os
import sys
import subprocess


def is_adb_running():
    os.system("adb kill-server")
    try:
        exit_code = os.system('adb devices > /dev/null 2>&1')
        if exit_code == 0:
            return True
    except OSError:
        pass
    return False

def get_package_info(serial):
    device = adbutils.adb.device()
    info = device.package_info(args.package)
    print("\n[+] Package info: ", info)

def list_devices():
    devices = adbutils.adb.devices()
    device_list = [device.serial.strip() for device in devices]
    if len(device_list) == 0:
        print("\n[+] No devices found.")
        exit()
    elif len(device_list) > 1:
        print("\n[+] Only one device is allowed.")
        exit()
    else:
        print("[+] Devices: ")
        print(device_list[0])
        get_package_info(device_list[0])

def create_project_folder():
    folder_path = 'projects'
    current_dir = os.getcwd()
    if os.path.isdir(folder_path):
        return
    else:
        print("\n[+] Folder does not exist. Creating new projects folder at location '" + current_dir + "/projects'")
        os.system("mkdir projects")

def create_project(project_name):
    folder_path = 'projects/' + project_name
    current_dir = os.getcwd()
    if os.path.isdir(folder_path):
        return
    else:
        print("\n[+] Folder does not exist. Creating new project at location '" + current_dir + "/projects" + "/" + args.package + "'")
        os.system("mkdir " + folder_path)

def download_content(folder_name):
    source_folder_path = f"/data/data/{folder_name}"
    current_dir = os.getcwd()
    destination_folder_path = f"{current_dir}/projects/{folder_name}"
    command = f"adb shell su -c 'ls -d {source_folder_path}/*/'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    create_command = f"adb shell su -c 'mkdir /sdcard/{folder_name}'"
    subprocess.run(create_command, shell=True)
    output_lines = result.stdout.splitlines()
    for line in output_lines:
        directory_name = line.strip().split("/")[-2]
        print(directory_name)
        pull_command = f"adb shell su -c 'cp -r {source_folder_path}/{directory_name} /sdcard/{folder_name}'"
        subprocess.run(pull_command, shell=True)
        pull_command = f"adb pull /sdcard/{folder_name}/{directory_name} {destination_folder_path}"
        subprocess.run(pull_command, shell=True)
    print("\n[+] Directories pulled:")
    for line in output_lines:
        directory_name = line.strip().split("/")[-2]
        print(directory_name)

def check_folder(folder_name):
    command = f"adb shell su -c 'ls /data/data/{folder_name}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    folder_exists = (result.returncode == 0)
    if folder_exists:
        print(f"\n[+] The package '{folder_name}' exists in /data/data. Pulling now...")
    else:
        print(f"\n[+] The package '{folder_name}' does not exist in /data/data. Exiting...")
        exit()

def list_packages():
    command = f"adb shell su -c 'ls /data/data/'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_lines = result.stdout.splitlines()
    print("\n[+] Listing all available packages:")
    for line in output_lines:
        directory_name = line.strip().replace('-', '').replace('[', '').replace(']', '')
        if directory_name and not directory_name.isspace() and '/' not in directory_name:
            print(directory_name)

def update_package(folder_name):
    print("[+] Pushing changes please wait.")
    current_dir = os.getcwd()
    source_folder_path = f"{current_dir}/projects/{folder_name}"
    target_folder_path = f"/sdcard/"
    push_command = f"adb push {source_folder_path} {target_folder_path}"
    subprocess.run(push_command, shell=True)
    target_folder_path2 = f"/sdcard/{folder_name}"
    push_command2 = f"adb shell su -c 'cp -r {target_folder_path2} /data/data'"
    subprocess.run(push_command2, shell=True)
    remove_command = f"adb shell su -c 'rm -r {target_folder_path2}'"
    subprocess.run(remove_command, shell=True)

parser = argparse.ArgumentParser(description='Pull all apk data')
parser.add_argument('-p', '--package', type=str, help='Package name')
parser.add_argument('-u', '--update', type=str, help='Update package data')
parser.add_argument('-l', '--list', action='store_true', help='List all packages')


args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if len(sys.argv) > 3:
    parser.print_help()
    sys.exit(1)

if args.package and is_adb_running():
    list_devices()
    check_folder(args.package)
    create_project_folder()
    create_project(args.package)
    download_content(args.package)
elif args.list:
    list_packages()
elif args.update:
    update_package(args.update)
else:
    print("\n[+] ADB is not running.")
