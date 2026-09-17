pyinstaller --onefile --icon=icon.ico -n "machineReports" --add-data "scripts;scripts" --add-data "scripts/libusb-1.0.dll;." --add-data "scripts/usb.ids;." main.py

pyinstaller --onefile --icon=icon.ico -n "machineReports" --add-data "scripts;scripts" --add-data "scripts/libusb-1.0.dll;." --add-data "scripts/usb.ids;." --hidden-import shellingham._core --hidden-import shellingham._windows main.py
