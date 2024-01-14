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

class Tor:
    def __init__(self):
        # Proxies configuration
        self.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

    def install_tor_windows(self):
        """
        Install Tor on Windows using Chocolatey package manager.
        """
        try:
            os.system("choco install tor")
            os.system("tor")
        except Exception as e:
            raise InstallationError("Failed to install Tor on Windows") from e

    def install_tor_linux(self):
        """
        Install Tor on Linux using apt-get package manager.
        """
        try:
            os.system("sudo apt-get install tor")
            os.system("sudo service tor start")
        except Exception as e:
            raise InstallationError("Failed to install Tor on Linux") from e

    @property
    def is_tor_installed(self):
        """
        Check if Tor is installed.

        Returns:
            bool: True if Tor is installed, False otherwise.
        """
        if os.name == "nt":  # Windows
            result = subprocess.run(["where", "tor"], capture_output=True, text=True)
        else:  # Linux
            result = subprocess.run(["which", "tor"], capture_output=True, text=True)
        return result.returncode == 0
    
    def renew_ip(self):
        """
        Renew the IP address by restarting the Tor service.
        """
        try:
            if os.name == "nt":  # Windows
                os.system("tor --service stop")
            else:  # Linux
                os.system("sudo service tor stop")
            time.sleep(3)
            if os.name == "nt":  # Windows
                os.system("tor")
            else:  # Linux
                os.system("sudo service tor start")
        except Exception as e:
            raise ConnectionError("Failed to renew IP address") from e

    def start_tor(self):
        """
        Start the Tor service.
        """
        try:
            if os.name == "nt":  # Windows
                os.system("tor")
            else:  # Linux
                os.system("sudo service tor start")
        except Exception as e:
            raise ConnectionError("Failed to start Tor service") from e

    def get_ip(self):
        """
        Get the current IP address using an external API.

        Raises:
            requests.exceptions.RequestException: If there is an error in making the request.
            IPError: If there is an error in retrieving the IP address.

        Returns:
            str: The current IP address.
        """
        try:
            response = requests.get('https://api.myip.com', proxies=self.proxies)
            response.raise_for_status()
            ip = response.json()["ip"]
            print(f"Your IP is: {ip}")
            return ip
        except requests.exceptions.RequestException as e:
            raise IPError("Failed to get IP address") from e

    def get_session(self):
        """
        Get a new requests Session object with configured proxies.

        Raises:
            ConnectionError: If there is an error in renewing the IP address.
            SessionError: If there is an error in creating the session.

        Returns:
            requests.Session: A Session object with configured proxies.
        """
        try:
            self.renew_ip()
            time.sleep(1)
            session = requests.Session()
            session.proxies = self.proxies
            return session
        except ConnectionError as e:
            raise SessionError("Failed to create session") from e



