import argparse
from loguru import logger
from functools import wraps
from time import perf_counter
from requests import post
from magic import Magic
from os.path import basename

def Loger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        logger.info(f"function start: ({func.__name__}) with parameters: {args} :\n")
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info(f"The function ({func.__name__}) ended with the result: {result}")
            logger.info(f"The function ({func.__name__}) has been completed for {(perf_counter() - start):.4f}\n")
        except Exception:
            logger.exception(f"the function ({func.__name__}) ended with an error\n")
        return result
    return wrapper

def createArgParser():
     parser = argparse.ArgumentParser(prog="ServerClient", 
                                      description="Interaction client for saving parameters \
                                                  to the server and viewing them",
                                      epilog="The client can be used with only one of the given arguments")
     parser.add_argument("uploadOrList", nargs = 1, type = str, choices=["upload", "list"],
                         help = "Selecting the action required from the client, (list) displaying the list \
                                 of songs on the server, (upload) uploading the song")
     parser.add_argument("uploadPath", nargs = '?', type = str, default=None,
                         help = "Path to uploading file")
     return parser

@Loger
def uploadFileToServer(path:str):
    with open(path, "rb") as buffer:
        file = {"file": (basename(path), buffer, Magic(mime=True).from_file(path))}
        logger.info(post("http://localhost:8888/upload", files=file).json)

@Loger
def printMusicListFromServer():
    musicList = post("http://localhost:8888/getListMusic").json()
    for music in musicList:
        print(music)
    print()
    
@Loger    
def main():
    parser = createArgParser()
    args = parser.parse_args()
    if args.uploadOrList[0] == "list":
        printMusicListFromServer()
    elif args.uploadOrList[0] == "upload" and args.uploadPath:
        uploadFileToServer(args.uploadPath)
    else:
        logger.error("Wrong arguments: upload should be followed by the path to the file")

if __name__ == "__main__":
    logger.info("Start work client")
    main()