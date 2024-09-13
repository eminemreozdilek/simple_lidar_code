import subprocess
import sys


def connect_usb_to_wsl():
    executable_path = 'usbipd list'

    arguments = ['list']

    result = subprocess.run([executable_path] + arguments, capture_output=True, text=True)

    if result.returncode == 0:
        print("Output:")
        print(result.stdout)
    else:
        print("Error:")
        print(result.stderr)


if __name__ == '__main__':
    connect_usb_to_wsl()
