import os
def check():
    if os.name == 'nt':
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return (False)
        else:
            return (True)
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (True)
        else:
            return (False)