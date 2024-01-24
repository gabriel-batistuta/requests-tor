import subprocess

def up_tor(file_path):
    subprocess.call(["sudo", "tor", "-f", f"{file_path}"])

up_tor('./tor_port')