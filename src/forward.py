import os
from fastapi import Request
from liulianmao import get_user_folder, PROJECT_FOLDER
from loguru import logger

async def forward_chat(request: Request):
    """
    处理聊天请求并转发给相应的模型
    """
    try:
        data = await request.json()
        model = data.get("model")
        messages = data.get("messages")
        # 处理并转发请求的逻辑
        response = {
            "model": model,
            "data": messages,
            "object": "list",
            "usage": {
                "completion_tokens": 0,
                "prompt_tokens": 100,
                "total_tokens": 100
            }
        }
    except Exception as e:
        logger.error(e)
        response = {}
    return response

async def forward_embedding(request: Request):
    """
    处理嵌入请求并转发给相应的模型
    """
    try:
        data = await request.json()
        model = data.get("model")
        input_text = data.get("input")
        # 处理并转发请求的逻辑
        response = {
            "model": model,
            "data": [
                {
                    "embedding": [
                        -0.02675454691052437,
                        0.019060475751757622,
                        -0.005519774276763201,
                        0.014949671924114227
                    ],
                    "index": 0,
                    "object": "embedding"
                }
            ],
            "object": "list",
            "usage": {
                "completion_tokens": 0,
                "prompt_tokens": 100,
                "total_tokens": 100
            }
        }
    except Exception as e:
        logger.error(e)
        response = {}
    return response
