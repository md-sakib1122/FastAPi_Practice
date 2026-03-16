from tempfile import SpooledTemporaryFile

from fastapi import FastAPI, File ,UploadFile , Request
from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 5
app = FastAPI()

@app.post("/upload")
async def red_file1(file: UploadFile = File(...)):
      content = file._in_memory
      whole = await file.read()
      chunk = await file.read(1024)
      print(content)
      #
      #     Client
      #       ↓
      # HTTP request stream
      #       ↓
      # multipart parser
      #       ↓
      # SpooledTemporaryFile (Spooled means temporary storage)
      #     ├── small data → RAM
      #     └── large data → temporary disk file
      #       ↓
      # UploadFile wrapper
      #       ↓
      # your endpoint
      #
      # .........ex............
      # Client uploads 5GB video
      #           ↓
      # Server stores temp file
      #           ↓
      # Your code reads file
      #           ↓
      # Upload to cloud
      #
      # [Disk usage = 5GB temporarily]
      #

@app.post("/upload-byte")
async def upload_byte(file: bytes = File(...)):
   content = file
   print(content)

   #      Client
   #         ↓
   #    HTTP request
   #         ↓
   #  multipart parser
   #         ↓
   #  ENTIRE FILE Read  into RAM
   #         ↓
   # converted to Python bytes
   #         ↓
   # passed to endpoint
   # Example if file = 200MB -> RAM usage = 200MB
@app.post("stream-upload")
async def stream_upload(request: Request):
     async for data in request.stream():
          print(data)


           # Here you bypass FastAPI's file system completely.
           #
           # No File()
           # No UploadFile
           #
           # You directly read the HTTP body stream.
           #
           # ............ex.............
           # Client uploads 5GB video
           #     ↓
           # FastAPI receives chunk
           #     ↓
           # Immediately send to cloud
           #     ↓
           # Next chunk
           #
           # [ Disk usage = 0 ,RAM usage = very small ]
           #
