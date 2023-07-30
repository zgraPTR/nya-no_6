"""設定ファイルを保存する
Configクラスの内容がファイルに保存される
"""

from modules import Pick


config_dict = {"is_owner": ["947380475389947944", "555729675213602816"]}


def main():
    """実行"""

    run_def = input("\n0 : 読み込み\n1 : 書き込み\n数字を入力 : ")

    print("\n")

    pickle_ = Pick("config.bin")
    if run_def == "0":
        data = pickle_.read()
        print(data)
    elif run_def == "1":
        pickle_.write(config_dict)
        print("書き込みが完了しました。")


if __name__:
    main()
