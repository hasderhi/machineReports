import os
import sys
import usb.core
import usb.util

# Explicitly set backend DLL path (libusb-1.0.dll)
if sys.platform == "win32":
    import usb.backend.libusb1

    # Adjust this path if needed
    DLL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "libusb-1.0.dll"))
    if not os.path.exists(DLL_PATH):
        raise FileNotFoundError(f"Missing libusb backend DLL at: {DLL_PATH}")

    backend = usb.backend.libusb1.get_backend(find_library=lambda x: DLL_PATH)
else:
    backend = None  # Let pyusb auto-detect on non-Windows systems

USB_IDS_FILE = os.path.join(os.path.dirname(__file__), 'usb.ids')

def load_usb_ids(path=USB_IDS_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing '{path}'. Download it from http://www.linux-usb.org/usb.ids"
        )
    vendors = {}
    current_vendor = None
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            if not line.startswith('\t'):
                parts = line.strip().split('  ', 1)
                if len(parts) == 2:
                    vid, name = parts
                    vid = vid.lower()
                    vendors[vid] = {'name': name.strip(), 'products': {}}
                    current_vendor = vid
            else:
                parts = line.strip().split('  ', 1)
                if len(parts) == 2 and current_vendor:
                    pid, name = parts
                    pid = pid.lower()
                    vendors[current_vendor]['products'][pid] = name.strip()
    return vendors

def get_usb_device_name(vid, pid, usb_ids):
    vid_hex = f"{int(vid):04x}"
    pid_hex = f"{int(pid):04x}"
    vendor = usb_ids.get(vid_hex, {}).get('name', f"Unknown Vendor ({vid_hex})")
    product = usb_ids.get(vid_hex, {}).get('products', {}).get(pid_hex, f"Unknown Product ({pid_hex})")
    return vendor, product

def list_usb_devices():
    try:
        usb_ids = load_usb_ids()
    except FileNotFoundError as e:
        return str(e)

    devices = usb.core.find(find_all=True, backend=backend)
    result = []

    for device in devices:
        vid = device.idVendor
        pid = device.idProduct
        try:
            vendor, product = get_usb_device_name(vid, pid, usb_ids)
        except Exception:
            vendor, product = f"VID: {vid:04x}", f"PID: {pid:04x}"
        result.append(f"{vendor} - {product} (VID: {vid:04x}, PID: {pid:04x})")

    return "\n".join(result)

list_usb_devices()
