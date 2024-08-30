import os

from fastapi import Request
from liulianmao import PROJECT_FOLDER, ask, get_user_folder
from loguru import logger

from const import const_model_mapping


async def forward_chat(request: Request):
    """
    处理聊天请求并转发给相应的模型
    """
    # 使用 await 来获取请求体中的 JSON 数据
    body = await request.json()
    logger.debug(body)
    conversation = body.get("messages")
    logger.trace(body)

    # ask() 不是异步的，返回简单字符串
    ans = ask(
        msg=conversation[0]["content"],
        available_models=body.get("available_models", ["gpt-4o"]),
        model_series=body.get(
            "model_series",
            "openai" if "glm" not in body.get("model") else "zhipu",
        ),
        no_history=True,
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
        return str(e)
