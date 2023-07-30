"""暗号化用モジュール
"""


class Xor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def crypto_text_to_hex(src_text, key):
        """暗号化 : 引数の2つの文字列をXORした結果をhex文字列で返す
        Args:
            src_text (str): 暗号化したい文字列
            key (str): 暗号化するためのキー文字列
        """
        xor_code = (key * ((len(src_text) // len(key)) + 1))[: len(src_text)]
        encrypted_data = "".join(
            [chr(ord(data) ^ ord(code)) for (data, code) in zip(src_text, xor_code)]
        )
        return encrypted_data.encode().hex()

    @staticmethod
    def decrypto_hex_to_text(hex_text, key) -> str:
        """複号: 引数のHex文字列とkeyをXORして戻した文字列で返す
        Args:
            hex_text (str): 暗号化されているhex文字列
            key (str): 複号するためのキー文字列
        """
        try:
            crypt_data = bytes.fromhex(hex_text).decode()
        except ValueError:
            return ""

        xor_code = (key * ((len(crypt_data) // len(key)) + 1))[: len(crypt_data)]
        decrypted_data = "".join(
            [chr(ord(data) ^ ord(code)) for (data, code) in zip(crypt_data, xor_code)]
        )
        return decrypted_data
