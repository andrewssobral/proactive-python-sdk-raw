import os
import proactive
import getpass

from dotenv import load_dotenv
load_dotenv()

def getProActiveGateway():
    print("Logging on proactive-server...")
    proactive_url = os.getenv("PROACTIVE_URL")
    if not proactive_url:
        proactive_url = input("Server (default: https://try.activeeon.com:8443): ")
    if proactive_url == "":
        proactive_url  = "https://try.activeeon.com:8443"
    if not proactive_url.startswith("http"):
        proactive_url  = "https://"+proactive_url+".activeeon.com:8443"
    print("Connecting on: " + proactive_url)
    gateway = proactive.ProActiveGateway(base_url=proactive_url)
    username = os.getenv("PROACTIVE_USERNAME")
    password = os.getenv("PROACTIVE_PASSWORD")
    if not (username and password):
        username = input("Login: ")
        password = getpass.getpass(prompt="Password: ")
    gateway.connect(username, password)
    assert gateway.isConnected() is True
    print("Connected")
    return gateway
