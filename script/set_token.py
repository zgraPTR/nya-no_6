"""Discord Bot Token設定
実行してTokenを暗号化してファイルに保存。Key忘れたら詰むから注意
Xor暗号化 -> https://qiita.com/magiclib/items/fe2c4b2c4a07e039b905
"""

from modules import Pick, Xor


def main():
    """_summary_"""
    pickle_ = Pick("token.bin")
    xor = Xor()

    token = pickle_.read()

    token_key = input("\nToken Key : ")
    if token:
        token_decrypto = xor.decrypto_hex_to_text(token, token_key)
        print("\nDiscord Token : ", token_decrypto)
        print("Tokenを変更したい場合は assets/config/token.bin を削除してください。")
    else:
        token = input("\nDiscord Bot Token : ")
        # 暗号化して保存
        token_crypto = xor.crypto_text_to_hex(token, token_key)
        pickle_.write(token_crypto)
        print("Tokenをセットしました。")


if __name__:
    main()
