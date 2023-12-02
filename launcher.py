"""ランチャー
python launcher.py [args]

agrs:
    0: bot実行
    1: ZIP送信
    2: ZIP解凍
"""

from ftplib import FTP
import os
import subprocess
import shutil
import sys
import zipfile

# スクリプトのディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = os.path.basename(__file__)

ZIP_DIR = "./bot"
ZIP_NAME = "bot"
ZIP_FILENAME = "bot.zip"


class Zip:
    """zipファイルの作成と解凍を行うクラス"""

    def make_zip(self):
        """zipファイルの作成"""

        shutil.make_archive(ZIP_NAME, "zip", root_dir=ZIP_DIR)

    def unpack_zip(self):
        """zipファイルの解凍"""

        with zipfile.ZipFile(ZIP_FILENAME) as existing_zip:
            existing_zip.extractall(ZIP_DIR)


class Ftps:
    """FTPクラス"""

    def __init__(self):
        """初期化"""

        self.ftp = FTP(timeout=10)
        self.ftp.connect(host="192.168.11.30", port=5049)
        self.ftp.login(user="pc", passwd="0000")
        self.ftp.set_pasv(True)

    def send_zip(self):
        """zipファイルをFTPで送信"""

        zip_file = Zip()
        zip_file.make_zip()

        self.ftp.cwd("/device/bot")
        with open(ZIP_FILENAME, "rb") as botzip:
            self.ftp.storbinary(f"STOR {ZIP_FILENAME}", botzip)
        with open(FILE_PATH, "rb") as lancherfile:
            self.ftp.storbinary(f"STOR {FILE_PATH}", lancherfile)


class InputFunction:
    """分岐処理を行うクラス"""

    def unpack(self):
        """zipファイルを解凍する関数"""

        # フォルダ削除
        shutil.rmtree("bot/")

        zip_file = Zip()
        zip_file.unpack_zip()
        print("\nリロード成功\n")

    def zip(self):
        """zipファイルを作成してFTPで送信する関数"""

        cftp = Ftps()
        cftp.send_zip()
        print("\nZIP送信成功\n")

    def run(self):
        """Botをサブプロセスで実行する"""

        token_key = input("\nToken Key : ")

        is_loop = True
        while is_loop:
            process = subprocess.Popen(
                ["python", "./bot/run.py", token_key],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    print(line, end="")

            os.system("clear")

            returncode = process.returncode
            if returncode == 5:
                InputFunction().unpack()
            if returncode != 5:
                is_loop = False
                print("\n実行が終了しました。")


def if_function(args):
    """引数を処理する関数"""
    input_actions = {
        "0": InputFunction().run,
        "1": InputFunction().zip,
        "2": InputFunction().unpack,
    }

    action = input_actions.get(args, main)
    action()


def main():
    """メイン関数"""

    if len(sys.argv) < 2:
        print("\n実行 : 0\nZIP送信 : 1\n解凍 : 2\n")
        argv = input("\n数字を入力 : ")
    else:
        argv = sys.argv[1]

    if_function(argv)


if __name__ == "__main__":
    main()
