import os

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, HTMLResponse
from liulianmao import ask
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
    logger.critical(body)
    model = body.get("model")
    messages = body.get("messages")

    # ask不是异步的，返回简单字符串
    ans = ask(
        msg=messages[0]["content"],
        available_models=[],
        model_series="openai",
        no_history=False,
        image_type="none",
    )
    print(ans)
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
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.post("/paas/v1/chat/completions")
async def pass_v1_chat_completions(request: Request):
    return forward_chat(request)


@app.post("/paas/v4/chat/completions")
async def pass_v4_chat_completions(request: Request):
    return await forward_chat(request)


@app.post("/embedding")
async def create_embedding(request: Request):
    return await forward_embedding(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
