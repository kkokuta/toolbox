import os

def safe_open(file_path, mode, *args, **kwargs):
    # ファイルが含まれるディレクトリを取得
    dir_path = os.path.dirname(file_path)

    # ディレクトリが存在しない場合は作成
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        pass

    # ファイルをオープンして返す
    return open(file_path, mode=mode, *args, **kwargs)