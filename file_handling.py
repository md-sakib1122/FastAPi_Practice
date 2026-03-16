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

      """
      MULTIPART: While a single file does have metadata (name, type), that isn't why the protocol 
      is named "multipart." The name comes from the fact that the HTTP body is physically
      divided into separate sections.
      
      1. What is the Multipart Parser?
      Think of the multipart parser as a "sorting machine" for a messy delivery truck.
      When a client sends a file, the HTTP request body isn't just the file bytes. 
      It’s a single continuous stream of data containing:
    
        1.Boundary markers (unique strings used to separate parts).
    
        2.Form field names (e.g., "username").
    
        3.File metadata (filename, Content-Type).
    
        4.The actual binary content of the file.
    
      The multipart parser (specifically the python-multipart library that FastAPI uses 
      under the hood) sits between the raw network socket and your code. Its job is to:
    
        1.Detect Boundaries: Find where one piece of data ends and the next begins.
    
        2.Extract Metadata: Pull out the filename and headers.
    
        3.Stream to Storage: Feed the binary chunks into the SpooledTemporaryFile.
      """

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
