"""設定ファイルを保存する
Configクラスの内容がファイルに保存される
"""

from modules import JsonManager


config_dict = {"owner_id": ["947380475389947944", "555729675213602816"]}


def main():
    """実行"""

    run_def = input("\n0 : 読み込み\n1 : 書き込み\n\n数字を入力 : ")

    print("\n")

    jm = JsonManager("config.json")
    if run_def == "0":
        data = jm.read()
        print(data)
    elif run_def == "1":
        jm.write(config_dict)
        print("書き込みが完了しました。")


if __name__:
    main()
