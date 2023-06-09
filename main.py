from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from utils.video_util import *
import uvicorn
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, 'input/')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output/')
#TEMLATE_FOLDER = os.path.join(BASE_DIR, 'report.html')

# video feed and anomal score 
@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

# input 비디오 src
@app.get("/input/{fileName}")
async def full(fileName):
    path = INPUT_FOLDER + fileName

    if os.path.isfile(path):
        return StreamingResponse(get_stream_video(path), media_type="multipart/x-mixed-replace;boundary=frame")
    else:
        return 'error'
    
# output 비디오 src
@app.get('/emergency')
async def full(request : Request):
    path = OUTPUT_FOLDER + 'fight1.mp4'

    if os.path.isfile(path):
        return StreamingResponse(get_stream_video(path), media_type="multipart/x-mixed-replace;boundary=frame")
    else:
        return 'error'

@app.get('/report', response_class=HTMLResponse) 
async def report(request : Request):
    return FileResponse("templates/report.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
