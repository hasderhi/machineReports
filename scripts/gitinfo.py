import subprocess

def get_git_info():
    def run_git_command(args):
        try:
            result = subprocess.run(["git"] + args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def get_global_config_value(key):
        return run_git_command(["config", "--global", key])

    def get_global_config_list():
        config_output = run_git_command(["config", "--global", "--list"])
        if config_output:
            return dict(line.split("=", 1) for line in config_output.splitlines() if "=" in line)
        return {}

    def get_repo_info():
        repo_root = run_git_command(["rev-parse", "--show-toplevel"])
        if not repo_root:
            return None
        branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        remote_url = run_git_command(["config", "--get", "remote.origin.url"])
        return {
            "repo_root": repo_root,
            "branch": branch,
            "remote_url": remote_url
        }

    # Check if Git is installed
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_installed = False

    return f"""Git Installed: {git_installed}
        Username: {get_global_config_value("user.name") if git_installed else None}
        User email: {get_global_config_value("user.email") if git_installed else None}
        Global config: {get_global_config_list() if git_installed else {}}
        Repository information (If available): {get_repo_info() if git_installed else None}
    """
