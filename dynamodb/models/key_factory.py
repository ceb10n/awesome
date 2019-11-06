from .key_type import KeyType
from .key import Key


class KeyFactory:

    def create(self, info):
        keys = []

        if 'KeySchema' in info:
            table_keys = info['KeySchema']
            for key in table_keys:
                keys.append(
                    Key(
                        key['AttributeName'],
                        KeyType(key['KeyType'])))

        return keys
