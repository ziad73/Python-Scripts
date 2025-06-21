import os
from pathlib import Path

def generate_directory_tree(directory_path, ignore_list=None, output_file="directory_tree.txt"):
    """
    Generates a tree structure of the given directory, ignoring specified files/directories.
    
    Args:
        directory_path (str): Path to the directory to scan
        ignore_list (list): List of files/directories to ignore
        output_file (str): Name of the output file (default: "directory_tree.txt")
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            print(f"Error: Directory '{directory_path}' does not exist.")
            return

        if ignore_list is None:
            ignore_list = []

        with open(output_file, 'w', encoding='utf-8') as f:
            # Write the root directory name
            f.write(f"{path.name}/\n")
            
            # Start the recursive tree generation
            _generate_tree(path, f, ignore_list)
        
        print(f"Directory tree successfully generated in {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def _generate_tree(directory, file_handler, ignore_list, prefix='', is_last=False):
    """Recursive helper function to generate the tree structure"""
    try:
        contents = sorted(os.listdir(directory))
    except PermissionError:
        file_handler.write(f"{prefix}└── [Permission Denied]\n")
        return

    # Filter out ignored items
    contents = [item for item in contents if item not in ignore_list]

    for i, item in enumerate(contents):
        path = directory / item
        current_is_last = i == len(contents) - 1
        
        # Determine the current indentation
        if prefix == '':
            current_indent = '└── ' if current_is_last else '├── '
        else:
            current_indent = '    ' if is_last else '│   '

        file_handler.write(f"{prefix}{current_indent}{item}")
        
        if path.is_dir():
            file_handler.write("/\n")
            new_prefix = prefix + ('    ' if is_last else '│   ')
            _generate_tree(path, file_handler, ignore_list, new_prefix, current_is_last)
        else:
            file_handler.write("\n")

def get_ignore_list():
    """Gets list of files/directories to ignore from user input"""
    print("Enter files/directories to ignore (comma separated, or press Enter for none):")
    user_input = input().strip()
    if not user_input:
        return []
    return [item.strip() for item in user_input.split(',')]

if __name__ == "__main__":
    # Get directory path from user
    target_directory = input("Enter directory path: ").strip()
    
    # you can set it manually or just get it from user
    # ignore_list = [
    #     '__pycache__',
    #     '.git',
    #     '.idea',
    #     'venv',
    #     '.env',
    #     '*.pyc',
    #     '*.pyo',
    #     '*.pyd',
    #     'db.sqlite3'
    # ]
    # Get ignore list from user
    ignore_list = get_ignore_list()
    
    # Generate the tree
    generate_directory_tree(target_directory, ignore_list)