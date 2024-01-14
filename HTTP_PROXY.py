import requests
import random
from requests.exceptions import RequestException

class IPError(Exception):
    pass
  
class ConnectionError(Exception):
    pass
  
class InstallationError(Exception):
    pass

class SessionError(Exception):
    pass
  
class HTTP:
    def __init__(self, fn):
        """
        Initialize the HTTP class with proxy configuration.

        Args:
            fn (str): The filename of the file containing proxies.
        """
        self.proxies = [line.strip() for line in open(fn, "r", encoding="utf-8", errors="ignore")]

    def set_proxy(self):
        """
        Set a random proxy from the available proxies.
        """
        proxy = random.choice(self.proxies)
        self.proxy = proxy

    def get_ip(self):
        """
        Get the current IP address using an external API.

        Raises:
            RequestException: If there is an error in making the request.
            IPError: If there is an error in retrieving the IP address.

        Returns:
            str: The current IP address.
        """
        try:
            response = requests.get('https://api.myip.com', proxies=self.proxy)
            response.raise_for_status()
            ip = response.json()["ip"]
            print(f"Your IP is: {ip}")
            return ip
        except RequestException as e:
            raise IPError("Failed to get IP address") from e

    def get_session(self):
        """
        Get a new requests Session object with configured proxies.

        Raises:
            ConnectionError: If there is an error in setting the proxy.
            SessionError: If there is an error in creating the session.

        Returns:
            requests.Session: A Session object with configured proxies.
        """
        try:
            self.set_proxy()
            session = requests.Session()
            session.proxies = self.proxy
            return session
        except ConnectionError as e:
            raise SessionError("Failed to create session") from e
