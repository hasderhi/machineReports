import os

def find_config_files():
    home_dir = os.path.expanduser("~")
    config_files = [
        ".bashrc",
        ".zshrc",
        ".profile",
        ".bash_profile",
        ".gitconfig",
        ".vimrc",
        ".npmrc",
        ".condarc",
        ".pythonrc",
        ".inputrc",
        ".config/code/settings.json",  # VS Code settings (Linux/macOS)
    ]

    found_files = {}
    for file in config_files:
        full_path = os.path.join(home_dir, file)
        if os.path.exists(full_path):
            found_files[file] = full_path

    return found_files
