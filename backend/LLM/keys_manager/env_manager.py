import os
from dotenv import load_dotenv
from typing import Dict

class EnvManager:
    """
    Saves and loads provisioning key
    """
    env_name = "provisioning_key.env"
    env_header_name = "key_name"
    env_value_name = "key_value"

    def __init__(self):
        """
        Creates connection to .env files or exception
        """
        if not os.path.exists(self.env_name):
            raise Exception(".env not exist")
        
        # Needs to be loaded
        load_dotenv(self.env_name)

        self.key_name = os.getenv(self.env_header_name)
        self.key_value = os.getenv(self.env_value_name)

        if self.key_name == None:
            raise Exception("key name is not exist")
        
        if self.key_value == None:
            raise Exception("key is not exist")
    
    def set_key(self, key: str, name: str = "default"):
        """
        Save your key and name
        
        :param key: Provisioning key value
        :param name: Key name (default)
        """
        with open(self.env_name, "w") as file:
            file.write(f"{self.env_header_name}={name}\n")
            file.write(f"{self.env_value_name}={key}\n")
        
        self.key_name = name
        self.key_value = key

    def get_key(self) -> Dict:
        """
        Loads provisioning key from .env (loaded in constructor)

        return {name:"", value:""}
        """
        return {
            "name": self.key_name, 
            "value": self.key_value
        }