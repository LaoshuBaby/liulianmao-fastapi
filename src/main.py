import os

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, JSONResponse
from liulianmao import PROJECT_FOLDER, get_user_folder
from loguru import logger

from forward import forward_chat, forward_embedding

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
            "environment_variables": dict(os.environ),
        }
    except Exception as e:
        logger.error(e)
        system_info = {}
    return JSONResponse(system_info)


@app.get("/meow")
async def meow():
    """
    liulianmao 系列框架标志性API
    当liulianmao库检测到当前的endpoint能返回这个值时，便认为后端也用了liulianmao框架
    """
    return JSONResponse({"liulianmao": "meow"})


@app.post("/v1/chat/completions")
async def v1_chat_completions(request: Request):
    """
    OpenAI 兼容接口
    """
    return await forward_chat(request)


@app.post("/paas/v1/chat/completions")
async def pass_v1_chat_completions(request: Request):
    """
    Zhipu 兼容接口（官网文档已废弃，有人还在用）
    """
    return await forward_chat(request)


@app.post("/paas/v4/chat/completions")
async def pass_v4_chat_completions(request: Request):
    """
    Zhipu 现役接口（遵循官网文档）
    """
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
    return JSONResponse({"logs": log_list})


@app.get("/logs/{filename}")
async def logs_file(filename: str = Path()):
    log_folder_path = os.path.join(
        str(get_user_folder()), PROJECT_FOLDER, "logs"
    )
    file_path = os.path.join(log_folder_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Log file not found")
    return FileResponse(file_path)


if __name__ == "__main__":
    if os.environ.get("PORT"):
        working_port = os.environ.get("PORT", 8080)
    else:
        working_port = 9000
    uvicorn.run(app, host="0.0.0.0", port=working_port)
