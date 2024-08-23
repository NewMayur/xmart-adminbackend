import base64
import uuid
import jwt
from functools import wraps
from flask import jsonify, request
from server import app

import platform
import subprocess
import socket
import psutil  # For Windows

# def get_local_ip():
#     # Get a list of network interfaces
#     interfaces = psutil.net_if_addrs()
#     # Iterate through the interfaces to find the one with an IPv4 address
#     for interface in interfaces:
#         if interfaces[interface][0].family == socket.AF_INET:
#             # Return the IPv4 address of the first interface found
#             subnet_mask = interfaces[interface][0].netmask
#             ip = interfaces[interface][0].address
#             return ip, subnet_mask
#     return "Local IP not found"

# For windows
# def get_local_ip():
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)
    
#     interfaces = psutil.net_if_addrs()
#     for interface_name, interface_addresses in interfaces.items():
#         if interface_name.startswith('Ethernet'):  # Adjust the interface name as needed
#             for address in interface_addresses:
#                 if address.family == socket.AF_INET:
#                     return [ip_address, 'localhost'], address.netmask

#     return ip_address, None  # Return None if subnet mask is not found

def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address



def get_ssid_windows():
    try:
        # Use subprocess to run the netsh command to get the SSID
        output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        output = output.decode("utf-8").split("\n")
        for line in output:
            if "SSID" in line:
                ssid = line.split(": ")[1].strip()
                return ssid
    except subprocess.CalledProcessError:
        pass
    return "SSID not found"


def get_ssid_linux():
    try:
        # Use subprocess to run the iwconfig command and grep the SSID
        output = subprocess.check_output(["iwgetid", "--raw"])
        # Decode the output and remove any trailing newline characters
        ssid = output.decode("utf-8").strip()
        return ssid
    except subprocess.CalledProcessError:
        pass
    return "SSID not found"


def get_ssid():
    system = platform.system()
    if system == "Windows":
        return get_ssid_windows()
    elif system == "Linux":
        return get_ssid_linux()
    else:
        return "SSID not found"


def save_base64_file(data):
    file_name = str(uuid.uuid4())
    banner_img_location = "./static/" + file_name
    with open(banner_img_location, "wb") as fh:
        base64_str = data
        base64_str = base64_str.split(",")[1] if "," in base64_str else base64_str

        missing_padding = len(base64_str) % 4
        if missing_padding != 0:
            base64_str += "=" * (4 - missing_padding)
        fh.write(base64.decodebytes(base64_str.encode("utf-8")))
    return file_name


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f({}, *args, **kwargs)

    return decorated
