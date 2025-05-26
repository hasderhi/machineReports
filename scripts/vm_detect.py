import subprocess

def detect_vm():
    try:
        ps_script = """
        $cs = Get-WmiObject -Class Win32_ComputerSystem
        "$($cs.Manufacturer) $($cs.Model)"
        """
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip().lower()

        vm_keywords = ['vmware', 'virtualbox', 'kvm', 'xen', 'qemu', 'virtual', 'hyper-v', 'bochs', 'parallels']
        if any(keyword in output for keyword in vm_keywords):
            return "VM signature detected"
        else:
            return "No VM signature detected"
    except Exception as e:
        return f"Failed to detect VM: {e}"

print(detect_vm())
