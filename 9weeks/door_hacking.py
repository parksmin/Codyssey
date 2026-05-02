import itertools
import multiprocessing
import string
import time
import zipfile
import zlib
import sys

ZIP_FILE = 'emergency_storage_key.zip'
PASSWORD_FILE = 'password.txt'
CHARACTERS = string.digits + string.ascii_lowercase

def try_password(password):
    try:
        with zipfile.ZipFile(ZIP_FILE, mode='r') as zip_file:
            first_file = zip_file.namelist()[0]
            zip_file.read(first_file, pwd=password.encode('utf-8'))
        return password
    except (RuntimeError, zlib.error, zipfile.BadZipFile, IndexError, OSError):
        return None

def make_passwords(target_range):
    for first_char in target_range:
        for rest in itertools.product(CHARACTERS, repeat=5):
            yield first_char + ''.join(rest)

def save_password(password):
    with open(PASSWORD_FILE, mode='w', encoding='utf-8') as file:
        file.write(password)

def extract_zip(password):
    with zipfile.ZipFile(ZIP_FILE, mode='r') as zip_file:
        zip_file.extractall(pwd=password.encode('utf-8'))

def unlock_zip(target_range):
    start_time = time.time()
    attempt_count = 0

    print(f'탐색 범위 [{target_range}] 해독을 시작합니다.')
    print(f'시작 시간: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    
    try:
        with multiprocessing.Pool() as pool:
            for result in pool.imap_unordered(
                try_password,
                make_passwords(target_range),
                chunksize=1000,
            ):
                attempt_count += 1
                if attempt_count % 100000 == 0:
                    elapsed_time = time.time() - start_time
                    print(f'[{target_range[0]}~] 반복 회수: {attempt_count}, 진행 시간: {elapsed_time:.2f}초')

                if result is not None:
                    elapsed_time = time.time() - start_time
                    save_password(result)
                    extract_zip(result)
                    print(f'\n암호 해독 성공! 암호: {result}')
                    pool.terminate()
                    return result
    except Exception as error:
        print(f'오류 발생: {error}')
    return None

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    if len(sys.argv) > 1:
        unlock_zip(sys.argv[1])
    else:
        unlock_zip(CHARACTERS)