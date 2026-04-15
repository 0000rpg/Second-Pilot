from keys_manager.key_manager import KeyManager
from keys_manager.key_access import KeyStorage

class KeyProvider:
    """
    Manages to API keys access
    """
    def __init__(self):
        """
        Try to create all connections
        """
        self.key_manager = KeyManager()
        self.key_storage = KeyStorage()
        self._reload_keys()

    def get_key(self) -> str:
        """
        Provides not busy key
        """
        keys_list = self.key_storage.get_all_keys()

        try:
            self._clear_disabled()
            for key in keys_list["keys"]:
                if self._is_not_busy(key["hash"]) == True:
                    self.key_manager.toggle_key(key["hash"])
                    return key["hash"]
        except:
            # Debug
            print(keys_list)
        
        try:
            result_key = self.key_manager.create_key()
            self.key_manager.toggle_key(result_key)
            return result_key["hash"]
        except:
            # Debug
            print("Key creation failed")
            return "error"
        
    def free_key(self, hash: str) -> bool:
        """
        Use when you ended with usage
        
        :param hash: key hash
        """
        try:
            if self.key_storage.get_key(hash)["busy"]:
                self.key_manager.toggle_key(hash)
                return True
        except:
            print("Error with freeing key", hash)
        return False

    def _reload_keys(self) -> bool:
        """
        Change all keys to not busy
        """
        try:
            keys_list = self.key_storage.get_all_keys()

            for key in keys_list["keys"]:
                if key["busy"]:
                    self.key_manager.toggle_key(key["hash"])
                    
            return True
        except:
            return False

    def _is_not_busy(self, hash: str) -> bool:
        """
        Is busy = False
        
        :param hash: key hash
        """
        key = self.key_storage.get_key(hash)

        if key == {}: 
            return False
        
        try:
            if key["busy"] == False:
                return True
        except:
            return False
        return False
        
    def _is_disabled(self, hash: str) -> bool:
        """
        Disabled = True
        
        :param hash: key hash
        """
        key = self.key_manager.read_key(hash)

        if key == {}:
            return False
        
        try:
            if key["disabled"] == True:
                return True
        except:
            return False
        return False
    
    def _clear_disabled(self) -> bool:
        """
        Delete all disabled keys
        """
        try:
            available_keys = self.key_manager.get_keys_list()

            local_hash_list = {key["hash"] for key in self.key_storage.get_all_keys()["keys"]}
            global_hash_list = {key["hash"] for key in available_keys}

            hashes_to_delete = local_hash_list - global_hash_list

            for hash in hashes_to_delete:
                self.key_manager.delete_key(hash)

            for key in available_keys:
                if key["disabled"] == True:
                    self.key_manager.delete_key(key["hash"])
            return True
        
        except Exception as error:
            # Debug
            print("Clearing error: ", error)
            return False