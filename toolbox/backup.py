from pathlib import Path, PosixPath
from datetime import datetime
import logging
import shutil
from functools import wraps


class IncrementalBackup:
    """
    Incremental backup class.

    usage:
    ```
    with IncrementalBackup(src_dir=".", dst_dir="backup"):
        with open("test.txt", "w") as f:
            f.write("Hello, world!")
    ```

    This code will create a backup file `backup/test_YYYYMMDD_HHMMSS_ffffff.txt`.
    """

    def __init__(self, *, src_dir: str, dst_dir: str, silent: bool=False) -> None:
        self.src_dir: Path = Path(src_dir)
        self.dst_dir: Path = Path(dst_dir)
        self.silent: bool = silent

    @property
    def st_mtimes_info(self) -> set[tuple[PosixPath, float]]:
        return {
            (file_path, file_path.stat().st_mtime)
            for file_path 
            in self.src_dir.rglob("*") 
            if file_path.is_file()
        }

    def __enter__(self) -> None:
        self.enter_st_mtimes_info = self.st_mtimes_info

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            return

        enter_st_mtimes_info = self.enter_st_mtimes_info
        exit_st_mtimes_info = self.st_mtimes_info
        updated_st_mtimes_info = exit_st_mtimes_info - enter_st_mtimes_info

        for file_path, st_mtime in updated_st_mtimes_info:
            modified_datetime = datetime.fromtimestamp(st_mtime)

            relative_path = file_path.relative_to(self.src_dir)
            extention = relative_path.suffix
            path = relative_path.stem

            backup_path = self.dst_dir / f"{path}_{modified_datetime:%Y%m%d_%H%M%S_%f}{extention}"
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file_path, backup_path)
            if not self.silent:
                logging.info(f"Backup completed successfully! {file_path} -> {backup_path}")


def incremental_backup(*, src_dir: str, dst_dir: str, silent: bool=False):
    """
    Incremental backup decorator.

    usage:
    ```
    @incremental_backup(src_dir=".", dst_dir="backup")
    def main():
        with open("test.txt", "w") as f:
            f.write("Hello, world!")
    ```

    This code will create a backup file `backup/test_YYYYMMDD_HHMMSS_ffffff.txt` when the function `main` is finished.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with IncrementalBackup(src_dir=src_dir, dst_dir=dst_dir, silent=silent):
                return func(*args, **kwargs)
        return wrapper
    return decorator
