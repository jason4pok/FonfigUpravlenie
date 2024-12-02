import os
import sys
import zipfile
import shutil

history_log = []

def extract_virtual_fs(zip_path):
    if not zipfile.is_zipfile(zip_path):
        print(f"Error: {zip_path} is not a valid zip file.")
        sys.exit(1)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("virtual_fs")
    print("Virtual filesystem extracted to: virtual_fs")

def ls(current_dir):
    try:
        return "\n".join(os.listdir(current_dir))
    except FileNotFoundError:
        return f"Error: {current_dir} not found."

def cd(current_dir, target_dir, root_dir):
    if (target_dir == '.' or target_dir == '..') or target_dir.replace('.', '') != '':
        new_dir = os.path.normpath(os.path.join(current_dir, target_dir))
        
        if os.path.exists(new_dir) and os.path.commonpath([root_dir, new_dir]) == root_dir:
            if os.path.isdir(new_dir):
                return new_dir

    return f"Error: {target_dir} is not a directory."

def rm(current_dir, target):
    target_path = os.path.join(current_dir, target)

    if not os.path.exists(target_path):
        return f"Error: {target} does not exist."

    if os.path.isfile(target_path):
        os.remove(target_path)
        return f"File {target} removed."

    if os.path.isdir(target_path):
        try:
            os.rmdir(target_path)
            return f"Directory {target} removed."
        except OSError:
            try:
                shutil.rmtree(target_path)
                return f"Directory {target} and all its contents removed."
            except Exception as e:
                return f"Error removing {target}: {str(e)}"

    return f"Error: {target} is not a valid target for removal."

def exit_shell():
    return "Exiting shell..."

def execute_command(command, current_dir, root_dir):
    global updated_dir
    history_log.append(command)

    parts = command.strip().split()
    if len(parts) == 0:
        return "Error: No command provided."

    base_command = parts[0]

    if base_command == "exit":
        return exit_shell()

    elif base_command == "ls":
        return ls(current_dir)

    elif base_command == "cd":
        if len(parts) == 1:
            return "Error: 'cd' requires a target directory."

        target_dir = parts[1].strip()
        result = cd(current_dir, target_dir, root_dir)
        if not result.startswith("Error"):
            updated_dir = result
        return result

    elif base_command == "rm":
        if len(parts) == 1:
            return "Error: 'rm' requires a target file or directory."

        target = parts[1].strip()
        return rm(current_dir, target)

    elif base_command == "history":
        return "\n".join(history_log)

    else:
        return f"Unknown command: {command}"

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <user_name> <virtual_fs.zip> <start_script.txt>")
        return

    user_name = sys.argv[1]
    virtual_fs_zip = sys.argv[2]
    start_script = sys.argv[3]

    extract_virtual_fs(virtual_fs_zip)

    global updated_dir
    global root_dir
    root_dir = os.path.abspath("virtual_fs")
    updated_dir = root_dir

    if os.path.exists(start_script):
        with open(start_script, "r") as f:
            for line in f:
                command = line.strip()
                if command:
                    # Получение относительного пути от виртуального корня
                    current_dir_name = os.path.relpath(updated_dir, root_dir)
                    if current_dir_name == '.':
                        current_dir_name = "/virtual_fs"
                    else:
                        current_dir_name = f"/virtual_fs/{current_dir_name}"
                    print(f"{user_name}@shell: {current_dir_name} $ {command}")
                    print(execute_command(command, updated_dir, root_dir))

    while True:
        # Получение относительного пути от виртуального корня
        current_dir_name = os.path.relpath(updated_dir, root_dir)
        if current_dir_name == '.':
            current_dir_name = "/virtual_fs"
        else:
            current_dir_name = f"/virtual_fs/{current_dir_name}"
        command = input(f"{user_name}@shell: {current_dir_name} $ ")
        if command.strip():
            result = execute_command(command, updated_dir, root_dir)
            print(result)
            if result == "Exiting shell...":
                break

if __name__ == "__main__":
    main()
