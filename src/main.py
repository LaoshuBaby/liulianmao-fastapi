import os

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, JSONResponse
from liulianmao import PROJECT_FOLDER, get_user_folder
from loguru import logger

from forward import forward_chat, forward_embedding
from omniverse import get_omniverse_router

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


@app.api_route("/omniverse/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def omniverse_proxy(request: Request, path: str):
    """
    Omniverse 统一代理接口
    将所有以 /omniverse/ 开头的请求转发到配置的 endpoint
    
    示例:
    - /omniverse/v1/chat/completion -> {endpoint}/v1/chat/completion
    - /omniverse/paas/v4/response?token=12345678 -> {endpoint}/paas/v4/response?token=12345678
    
    配置:
    通过环境变量 OMNIVERSE_ENDPOINT 设置目标 endpoint
    例如: export OMNIVERSE_ENDPOINT=https://api.openai.com
    """
    try:
        router = get_omniverse_router()
        return await router.forward_request(request, path)
    except ValueError as e:
        # 当 OMNIVERSE_ENDPOINT 未设置时
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    import asyncio
    from omniverse import close_omniverse_router
    
    if os.environ.get("PORT"):
        working_port = os.environ.get("PORT", 8080)
    else:
        working_port = 9000
    
    # 配置 uvicorn 服务器
    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=working_port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    
    try:
        # 启动服务器
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        # 关闭 omniverse 路由器
        asyncio.run(close_omniverse_router())
        logger.info("Omniverse router closed.")
