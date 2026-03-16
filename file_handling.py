from tempfile import SpooledTemporaryFile

from fastapi import FastAPI, File ,UploadFile , Request
from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 5
app = FastAPI()

@app.post("/upload")
async def red_file1(file: UploadFile = File(...)):
     content = file._in_memory
     print(content)

@app.post("/upload-byte")
async def upload_byte(file: bytes = File(...)):
   content = file
   print(content)

@app.post("stream-upload")
async def stream_upload(request: Request):
     async for data in request.stream():
            print(data)


