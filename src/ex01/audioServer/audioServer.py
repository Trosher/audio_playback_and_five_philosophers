from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from functools import wraps
from loguru import logger
from time import perf_counter
from os import listdir
from uvicorn import run
from pathlib import Path
from magic import Magic
from shutil import copyfileobj
    
app = FastAPI()
templates = Jinja2Templates(directory='ui')

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

@Loger
def getListFile(patn_f):
    listFile = listdir(patn_f)
    return [file for file in listFile if Magic(mime=True).from_file(patn_f+file)[:5] == "audio"]

@Loger
def saveFile(file):
    with open(f"audio/{file.filename}", "wb") as buffer:
        copyfileobj(file.file, buffer)
    return True

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    listAudioFile = getListFile(str(Path(__file__).parent.resolve())+"\\audio\\")
    if not listAudioFile:
        logger.info("Audio files not found, check if there are files in the audio directory in the project directory")
    return templates.TemplateResponse("page.html", 
                                      {
                                          "request": request, 
                                          "listAudioFile":listAudioFile
                                      }
                                     )

@app.post("/getListMusic")
async def getListMusic():
    return getListFile(str(Path(__file__).parent.resolve())+"\\audio\\")

@app.post("/upload")
async def upload(file: UploadFile):
    status = 501
    messege = "File uploaded error"
    if file.content_type[:5] == "audio" and saveFile(file):
        status = 200
        messege = "File uploaded successfully"    
    return JSONResponse(content={"message": messege}, status_code=status)

@app.get("/audio/{filename}")
async def play_audio(filename: str):
    audio_file_path = f"audio/{filename}"
    
    if not Path(audio_file_path).is_file():
        return JSONResponse(content={"message": "no file on server"}, status_code=501)

    async def stream_file():
        with open(audio_file_path, "rb") as audio_file:
            chunk = audio_file.read(1024)
            while chunk:
                try:
                    yield chunk
                    chunk = audio_file.read(1024)
                except KeyboardInterrupt:
                    return
            
    return StreamingResponse(stream_file(), media_type="audio/mpeg")
    
if __name__ == '__main__':
    logger.info("Server started listening on port: 8888")
    run(app, host='127.0.0.1', port=8888, log_level="info")