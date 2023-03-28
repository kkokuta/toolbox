import psutil
import os

def get_caller_name(*, with_dir: bool = False, with_ext: bool = False) -> str:
    # 実行中の Python スクリプトのプロセスIDを取得
    pid = psutil.Process().ppid()

    # プロセスIDから親プロセス（つまり、シェルスクリプト）の情報を取得
    parent_process = psutil.Process(pid)

    # 親プロセスのコマンドラインを取得
    command_line = parent_process.cmdline()

    # コマンドラインからシェルスクリプトのファイル名を取得
    caller_filename = command_line[1]

    if not with_dir:
        caller_filename = os.path.basename(caller_filename)

    if not with_ext:
        caller_filename = os.path.splitext(caller_filename)[0]

    # シェルスクリプトのファイル名を返す
    return caller_filename