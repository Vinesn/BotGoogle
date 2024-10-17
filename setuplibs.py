import subprocess
import sys
import pkg_resources

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install(packages):
    for package in packages:
        try:
            pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            print(f"{package} is not installed. Installing...")
            install(package)

def auto_install():
    required_packages = [
        "pyautogui",
        "py4j",
        "pyperclip",
        "pymssql",
    ]
    check_and_install(required_packages)

if __name__ == "__main__":
    auto_install()
