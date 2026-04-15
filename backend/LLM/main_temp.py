from keys_manager.env_manager import EnvManager
from keys_manager.key_manager import KeyManager
from keys_manager.key_access import KeyStorage
from keys_manager.key_distributor import KeyProvider
from logger.logger import log
import json
import ast

def validate_json(text):
    try:
        json.loads(text)
        print("Valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        print(f"Error at position {e.pos}: {repr(text[max(0, e.pos-20):e.pos+20])}")
        return False

def main():
    '''
    my_provider = KeyProvider()

    for i in range(5):
        my_provider.get_key()
    '''

    print(log())


    texter = ''
    with open("test_text.txt", "r", encoding="utf-8-sig") as file:
        texter = file.read()
    

    texter = texter.strip()
    validate_json(texter)
    jtext = ''
    jtext = json.dumps(ast.literal_eval(texter), indent=4)
    print(jtext)


if __name__ == '__main__':
    main()
