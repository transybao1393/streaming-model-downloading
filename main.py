import requests
import logging
import threading
from tqdm import tqdm

URL = "https://instagram.com/favicon.ico"
WEIGHTS_URL = "https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov7-tiny.weights"
CFG_URL = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov7-tiny.cfg"

def download_file():
    # start threading
    weights = threading.Thread(target = download, args=(WEIGHTS_URL, "yolov7-tiny.weights",))
    
    cfg = threading.Thread(target = download, args=(CFG_URL, "yolov7-tiny.cfg",))
    cfg.start()
    weights.start()
    cfg.join()
    weights.join()
    
    
# simple stle
def file_download(URL: str, file_name: str):
    response = requests.get(URL)
    open(file_name, "wb").write(response.content)

# download file with streaming mode and progress bar
def download(url: str, fname: str):
    try:
        # solution 1
        # resp = requests.get(url, stream=True)
        # total = int(resp.headers.get('content-length', 0))
        # Can also replace 'file' with a io.BytesIO object
        # with open(fname, 'wb') as file, tqdm(
        #     desc=fname,
        #     total=total,
        #     unit='iB',
        #     unit_scale=True,
        #     unit_divisor=1024,
        # ) as bar:
        #     for data in resp.iter_content(chunk_size=1024):
        #         size = file.write(data)
        #         bar.update(size)

        # solution 2
        with requests.get(url, stream=True) as r:
            total = int(r.headers.get('content-length', 0))
            # Can also replace 'file' with a io.BytesIO object
            with open(fname, 'wb') as file, tqdm(
                desc=fname,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
    except requests.exceptions.ConnectionError as ce:
        print("ConnectionError with message: ", ce)
    except requests.exceptions.FileModeWarning as fm:
        print("FileModeWarning with message: ", fm)
    except requests.exceptions.HTTPError as he:
        print("HTTPError with message: ", he)
    except requests.exceptions.Timeout as timeout:
        print("Timeout with message: ", timeout)
    except Exception as e:
        print("General exception with message: ", e)
    finally:
        # resp.close()
        print("Download complete!")
    

download_file()