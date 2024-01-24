from requests import Session
from random import randint
import json
import socket

def is_port_free(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(('localhost', port))
        print(f'The port: {port} is ocuped.')
        return False
    except socket.error:
        print(f'The port: {port} is free.')
        return True

def get_aleatory_port_number():
    port_number = randint(1000, 9999)
    return port_number

def get_port_number():
    port_number = get_aleatory_port_number()
    while is_port_free(port_number) == False:
        port_number = get_aleatory_port_number()
    return port_number

def create_tor_port(file_path, SOCKSPort, ControlPort):
    with open(file_path, 'w') as f:
        f.write(f"SOCKSPort {SOCKSPort} \n")
        f.write(f"ControlPort {ControlPort}\n")
        f.write(f"DataDirectory ./{SOCKSPort}\n")

def create_json_file(SOCKSPort, ControlPort):
    with open('.json', 'w') as secret_file:
        json.dump(
            {
                "SOCKSPort": SOCKSPort, 
                "ControlPort": ControlPort
            }
            ,secret_file, indent=4)

def get_proxy_port():
    ip_site = "http://httpbin.org/ip"
    site_content = request_website(ip_site)
    proxy_port = json.loads(site_content)["origin"]
    return proxy_port

def request_website(url):
    session = Session()
    session.proxies = {
        'http': f'socks5://localhost:{SOCKSPort}',
        'https': f'socks5://localhost:{SOCKSPort}'
    }
    response = session.get(url)
    return response.content

if __name__ == '__main__':
    try:
        with open('.json', 'r', encoding='utf-8') as secret_file:
            file_json = json.load(secret_file)
            SOCKSPort = file_json["SOCKSPort"]
            ControlPort = file_json["ControlPort"]
    except FileNotFoundError:
        SOCKSPort = get_port_number()
        ControlPort = get_port_number()
        create_tor_port('./tor_port', SOCKSPort, ControlPort)
        create_json_file(SOCKSPort, ControlPort)
        print("run up_tor.py and this after :)")
        exit()

    url = input("type a url: ")
    request_website(url)