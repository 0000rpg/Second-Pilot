import os
import json
from typing import Any, Dict, Optional

class KeyStorage:
    """
    Save | Load | Delete keys
    """

    def __init__(self, storage_name: str = "keys_storage.json", storage_path: str = ""):
        """
        Gets access to ALL keys or raises error
        """
        self.storage_name = f"{storage_path}{storage_name}"
        self.keys_storage = self._load_keys()

        if not os.path.exists(self.storage_name):
            # Debug
            print("Keys storage doesn't exist")
        
    def _load_keys(self) -> Dict[str, any]:
        """
        Returns current keys storage from files
        """
        if not os.path.exists(self.storage_name):
            return {}
        
        try:
            with open(self.storage_name, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}
        
    def _save_keys(self):
        """
        Saves keys to file
        """
        with open(self.storage_name, 'w') as file:
            json.dump(self.keys_storage, file, indent=4)
    
    def get_key(self, key_hash: str) -> Dict:
        """
        Get key by hash

        :param key_hash: key hash string
        """
        all_keys = self._load_keys()

        if all_keys == {}:
            return {}

        for key in all_keys["keys"]:
            if key["hash"] == key_hash:
                return key
            
        return {}

    def set_key(self, key: Dict):
        """
        Create new key

        :param key: dict-JSON key
        """
        if not (key["hash"] and key["label"] and key["name"]):
            # Debug
            print("Invalid key")
            return
         
        if self.keys_storage == {}:
            self.keys_storage = {"keys":[]}
        
        if self.get_key(key["hash"]):
            # Debug
            print("This key already exists")
            return
        
        self.keys_storage["keys"].append(key)
        self._save_keys()
    
    def get_all_keys(self) -> Dict:
        """
        Returns all keys or {}
        """
        return self._load_keys()
    
    def delete_key(self, hash: str) -> bool:
        """
        Delete key by hash

        :param key_hash: key hash string
        """
        if self.keys_storage == {}:
            # Debug
            print("Empty storage")
            return False
        
        for key in self.keys_storage["keys"]:
            if (key["hash"] == hash):
                self.keys_storage["keys"].remove(key)
                self._save_keys()
                return True
            
        return False
    
    def update_key(self, new_key: Dict) -> bool:
        """
        Update key by hash

        :param key_hash: key hash string
        """
        hash = new_key["hash"]

        if self.get_key(hash) == {}:
            # Debug
            print("Key doesn't exist")
            return False
        
        all_keys = self.keys_storage["keys"]

        for key in all_keys:
            if key["hash"] == hash:
                key.update(new_key)
                self._save_keys()
                return True
        
        # Debug
        print("Unexpected update error")
        return False