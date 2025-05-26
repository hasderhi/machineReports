import os

def get_envvars():
    envvars = os.environ
    formatted = "\n        ".join(f"{key} = {value}" for key, value in envvars.items())
    return formatted