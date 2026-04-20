from keys_manager.env_manager import EnvManager
from keys_manager.key_access import KeyStorage
from typing import Dict
import requests
import json
import secrets

class KeyManager:
    """
    CRUD with API keys
    """
    BASE_URL = "https://openrouter.ai/api/v1/keys"

    def __init__(self):
        """
        Gets access to provisioning key or raises error
        """
        try:
            self.provisioning_key_manager = EnvManager()
            self.provisioning_key = self.provisioning_key_manager.get_key()

        except Exception as error:
            # Debug
            print(error)
            raise Exception("Provisioning key: " + error)
        
        finally:
            self.key_storage = KeyStorage()
    
    def _rand_name(self):
        """
        Needs for autonaming. Using secrets but can use standart random.
        """
        return f"Key-#{secrets.token_hex(32)}"
    
    def _error_format(self, error: Dict) -> str:
        """
        Return pretty error string
        """
        return f"[ {error["error"]["code"]} ] {error["error"]["message"]}"
    
    def _merge_data(self, key: Dict, hash: str) -> Dict:
        """
        Returns merged data
        """
        key.update(self.key_storage.get_key(hash))
        return key
    
    def create_key(self, key_name: str="default") -> Dict:
        """
        Generate API key
        
        :return: Key: hash, label, name and busy.
        """
        if key_name == "default":
            key_name = self._rand_name()
        
        response = requests.post(
            f"{self.BASE_URL}",
            headers={
                "Authorization": f"Bearer {self.provisioning_key["value"]}",
                "Content-Type": "application/json"
            },
            json={
                "name": key_name
            }
        )

        response_result = json.loads(response.text)
        result_key = ""
        try:
            result_key = {
                "hash": response_result["data"]["hash"],
                "label": response_result["key"],
                "name": response_result["data"]["name"],
                "busy": False
            }
        except Exception as error:
            # Debug
            print("Key creation error: ", error)
            print(self._error_format(response_result))
            return {}
        
        self.key_storage.set_key(result_key)
        return result_key

    def delete_key(self, hash: str, mode: str="default") -> bool:
        """
        Delete key by hash
        
        :param hash: key hash stroke
        :param mode: delete only local keys by default
        :return: Success or not
        """
        successfull = False

        if mode == "default":
            if not self.key_storage.delete_key(hash):
                # Debug
                print("API key doesn't exist")
                return successfull
        
        response = requests.delete(
            f"{self.BASE_URL}/{hash}",
            headers={
                "Authorization": f"Bearer {self.provisioning_key["value"]}",
                "Content-Type": "application/json"
            }
        )

        response_result = json.loads(response.text)

        try:
            successfull = bool(response_result["deleted"])
        except:
            print(self._error_format(response_result))
        return successfull

    def read_key(self, hash: str) -> Dict:
        """
        Gives key state by hash
        
        :param hash: key hash stroke
        :return: key structure
        """
        response = requests.get(
            f"{self.BASE_URL}/{hash}",
            headers={
                "Authorization": f"Bearer {self.provisioning_key["value"]}",
                "Content-Type": "application/json"
            }
        )

        response_result = json.loads(response.text)

        try:
            self._merge_data(response_result["data"], hash)
            return response_result["data"]
        except:
            # Debug
            print(self._error_format(response_result))
        return {}  

    def toggle_key(self, hash: str) -> bool:
        """
        Gives key state by hash
        
        :param hash: key hash stroke
        :return: key structure
        """
        key = self.key_storage.get_key(hash)

        if key == {}:
            # Debug
            print("No available keys by hash")
            return False
        
        key["busy"] = not key["busy"]
        self.key_storage.update_key(key)
        return True

    def get_keys_list(self) -> Dict:
        """
        Returns all available keys (doesn't include unknown)
        """
        response = requests.get(
            self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.provisioning_key["value"]}",
                "Content-Type": "application/json"
            }
        )
        response_result = json.loads(response.text)
        result_list = []

        try:
            for key in response_result["data"]:
                hash = key["hash"]
                if self.key_storage.get_key(hash):
                    result_list.append(self._merge_data(key, hash))
            return result_list
        except:
            # Debug
            print(self._error_format(response_result))
        return {}