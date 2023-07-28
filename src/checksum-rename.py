import hashlib
import os
import sys
from concurrent.futures import ProcessPoolExecutor

def compute_shake_128(file_path: str, length: int = 12) -> str:
    """
    Compute the shake_128 checksum of a file.

    :param file_path: The path of the file to compute the shake_128 checksum for.
    :param length: The length of the shake_128 checksum in bytes.
    :return: The shake_128 checksum of the file.
    """
    shake_128 = hashlib.shake_128()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(128 * 1024)
            if not data:
                break
            shake_128.update(data)
    return shake_128.hexdigest(length)

def rename_file(file_path: str, length: int = 12) -> None:
    """
    Rename a file to its shake_128 checksum.

    If a file with the same name already exists, delete the original file if it is not 
    already named with its shake_128 checksum.

    :param file_path: The path of the file to rename.
    :param length: The length of the shake_128 checksum in bytes.
    """
    shake_128 = compute_shake_128(file_path, length)
    new_file_name = shake_128 + os.path.splitext(file_path)[1]
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    if os.path.exists(new_file_path):
        if os.path.basename(file_path) != new_file_name:
            os.remove(file_path)
    else:
        os.rename(file_path, new_file_path)

def main() -> None:
    """
    Main function.

    Takes as input the name of a folder from the command line, computes the shake_128 checksum 
    of each file in the folder and renames each file to its shake_128 checksum. 
    Uses multiprocessing from concurrent.futures to speed up the operation.
    """
    folder = sys.argv[1]  
    with ProcessPoolExecutor() as executor:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(rename_file, file_path)

if __name__ == '__main__':
    main()
