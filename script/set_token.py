"""Discord Bot Token設定
実行してTokenを暗号化してファイルに保存。Key忘れたら詰むから注意
Xor暗号化 -> https://qiita.com/magiclib/items/fe2c4b2c4a07e039b905
"""

from modules import JsonManager, Xor


def main():
    """_summary_"""
    jm = JsonManager("token.json")
    xor = Xor()

    token_dict = jm.read()

    if token_dict:
        token = token_dict.get("token", "不明")
        if token_dict.get("is_crypto", False):
            token_crypto_key = input("\nToken暗号キー : ")
            token = xor.decrypto_hex_to_text(token, token_crypto_key)
        print("\nDiscord Token : ", token)
        print("\nTokenを変更したい場合は assets/config/token.json を削除してください。")
        return

    token_dict = {"is_crypto": 0, "token": ""}

    token = input("\nDiscord Bot Token : ")
    is_decrypto = input("\n暗号化しますか? (y/n) : ")

    if is_decrypto == "y":
        token_dict["is_crypto"] = 1
        token_decrypto_key = input("\nToken暗号キー : ")
        token = xor.crypto_text_to_hex(token, token_decrypto_key)

    token_dict["token"] = token
    jm.write(token_dict)
    print("\n設定しました。")


if __name__:
    main()
