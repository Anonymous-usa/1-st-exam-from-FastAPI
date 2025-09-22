from pathlib import Path
import uuid

MEDIA_DIR = Path("./media")
MEDIA_DIR.mkdir(exist_ok=True)

async def save_file(file):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = MEDIA_DIR / filename
    try:
        # Save the file to the disk
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())
        
        return {"status": 200, "message": filename}  # Ensure "message" key is included
    
    except Exception as error:
        return {"status": 400, "error": str(error)}  # If error occurs, return error message
