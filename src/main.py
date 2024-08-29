import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, JSONResponse
from liulianmao import PROJECT_FOLDER, ask, get_user_folder
from loguru import logger

const_model_mapping = {
    "gpt-3-turbo": "glm-4",
    "gpt-4": "glm-4-0520",
    "gpt-4o": "glm-4v",
    "text-embedding-ada-002": "embedding-3",
}

app = FastAPI()


async def forward_chat(request: Request):
    # 使用 await 来获取请求体中的 JSON 数据
    body = await request.json()
    logger.debug(body)
    conversation = body.get("messages")
    logger.trace(body)

    # ask() 不是异步的，返回简单字符串
    ans = ask(
        msg=conversation[0]["content"],
        available_models=body.get("available_models", ["gpt-4o"]),
        model_series=body.get("model_series", "openai"),
        no_history=False,
        image_type="none",
        model=body.get("model"),
    )
    logger.debug(f"[ans]: {ans}")
    return ans


async def forward_embedding(request: Request):
    try:
        # 使用 await 来获取请求体中的 JSON 数据
        body = await request.json()
        model = body.get("model")
        input_text = body.get("input")

        if model in const_model_mapping:
            model = const_model_mapping[model]

        # ask不是异步的，返回简单字符串
        response = ask(msg=input_text, model=model)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def hello():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.get("/hello")
async def hello_route():
    system_info = {
        "os": os.name,
        "platform": os.sys.platform,
        "version": os.sys.version,
        "environment_variables": dict(os.environ)
    }
    return JSONResponse(content=system_info)


@app.post("/paas/v1/chat/completions")
async def pass_v1_chat_completions(request: Request):
    return await forward_chat(request)


@app.post("/paas/v4/chat/completions")
async def pass_v4_chat_completions(request: Request):
    return await forward_chat(request)


@app.post("/embedding")
async def create_embedding(request: Request):
    return await forward_embedding(request)


@app.get("/logs")
async def list_logdir(request: Request):
    log_folder_path = os.path.join(
        str(get_user_folder()), PROJECT_FOLDER, "logs"
    )
    try:
        log_list = os.listdir(log_folder_path)
        logger.debug(log_list)
    except Exception as e:
        logger.error(e)

    return JSONResponse({"logs":log_list})


@app.get("/logs/{filename}")
async def get_log_file(filename: str = Path(..., description="The name of the log file to retrieve")):
    log_folder_path = os.path.join(
        str(get_user_folder()), PROJECT_FOLDER, "logs"
    )
    file_path = os.path.join(log_folder_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Log file not found")
    return FileResponse(file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
