import pkg_resources

def list_packages():
    installed_packages = pkg_resources.working_set
    output = []
    for package in installed_packages:
        output.append(f"{package.key} > {package.version}")
    return '\n    '.join(map(str, sorted(output)))