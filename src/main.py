import os
import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, JSONResponse
from liulianmao import get_user_folder, PROJECT_FOLDER
from loguru import logger
from src.forward import forward_chat, forward_embedding
from src.const import const_model_mapping

app = FastAPI()

@app.get("/")
async def hello():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.get("/hello")
async def environment():
    try:
        system_info = {
            "os": os.name,
            "platform": os.sys.platform,
            "version": os.sys.version,
            "environment_variables": dict(os.environ)
        }
    except Exception as e:
        logger.error(e)
        system_info = {}
    return JSONResponse(content=system_info)

@app.post("/paas/v1/chat/completions")
async def pass_v1_chat_completions(request: Request):
    return await forward_chat(request)

@app.post("/paas/v4/chat/completions")
async def pass_v4_chat_completions(request: Request):
    return await forward_chat(request)

@app.post("/embedding")
async def embedding(request: Request):
    return await forward_embedding(request)

@app.get("/logs")
async def logs(request: Request):
    log_folder_path = os.path.join(
        str(get_user_folder()), PROJECT_FOLDER, "logs"
    )
    try:
        log_list = os.listdir(log_folder_path)
        logger.debug(log_list)
    except Exception as e:
        logger.error(e)
        log_list = []
    return JSONResponse({"logs": log_list})

@app.get("/logs/{filename}")
async def logs_file(filename: str = Path(..., description="The name of the log file to retrieve")):
    log_folder_path = os.path.join(
        str(get_user_folder()), PROJECT_FOLDER, "logs"
    )
    file_path = os.path.join(log_folder_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Log file not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
