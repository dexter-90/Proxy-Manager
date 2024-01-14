import os
import subprocess
import time
import requests

class IPError(Exception):
    pass
  
class ConnectionError(Exception):
    pass
  
class InstallationError(Exception):
    pass

class SessionError(Exception):
    pass

class NordVPN:
    def __init__(self, server="United States"):
        """
        Initialize NordVPN with a default server.

        Args:
            server (str): Name of the server to connect to (default: "United States").
        """
        self.server = server

    @property
    def is_nordvpn_installed(self):
        """
        Check if NordVPN is installed.

        Returns:
            bool: True if NordVPN is installed, False otherwise.
        """
        if os.name == "nt":  # Windows
            result = subprocess.run(["where", "nordvpn"], capture_output=True, text=True)
        else:  # Linux
            result = subprocess.run(["which", "nordvpn"], capture_output=True, text=True)
        return result.returncode == 0
    
    def connect(self):
        """
        Connect to a NordVPN server.

        Raises:
            ConnectionError: If an error occurs while connecting to NordVPN.
        """
        try:
            if os.name == "nt":  # Windows
                os.system(f"nordvpn -c -n {self.server}")
                
                while True:
                    time.sleep(20)
                    try:
                        self.get_ip()
                    except IPError:
                        continue

            else:  # Linux
                os.system(f"nordvpn -c -n {self.server}")

                while True:
                    time.sleep(20)
                    try:
                        self.get_ip()
                    except IPError:
                        continue

        except Exception as e:
            raise ConnectionError(f"Error connecting to NordVPN: {str(e)}")

    def disconnect(self):
        """
        Disconnect from the NordVPN server.

        Raises:
            ConnectionError: If an error occurs while disconnecting from NordVPN.
        """
        try:
            if os.name == "nt":  # Windows
                os.system("nordvpn disconnect")
                time.sleep(3)
            else:  # Linux
                os.system("nordvpn disconnect")
                time.sleep(3)
        except Exception as e:
            raise ConnectionError(f"Error disconnecting from NordVPN: {str(e)}")

    def get_ip(self):
        """
        Get the current public IP address.

        Raises:
            IPError: If an error occurs while getting the IP address.
        """
        try:
            response = requests.get('https://api.myip.com')
            ip = response.json()["ip"]
            print(f"Your IP is: {ip}")
        except Exception as e:
            raise IPError(f"Error getting IP address: {str(e)}")

    def get_session(self):
        """
        Renew IP and return a requests session with NordVPN proxy settings.

        Returns:
            requests.Session: A requests session object with NordVPN proxy settings.

        Raises:
            SessionError: If an error occurs while creating the session.
        """
        try:
            self.disconnect()
            self.connect()
            session = requests.Session()
            return session
        except Exception as e:
            raise SessionError(f"Error creating session with NordVPN: {str(e)}")
