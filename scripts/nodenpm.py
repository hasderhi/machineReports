import subprocess

def get_node_and_npm_versions():
    def get_version(command):
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    node_version = get_version(["node", "-v"])
    npm_version = get_version(["npm", "-v"])

    return {
        "node_version": node_version,
        "npm_version": npm_version
    }
