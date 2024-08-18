import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse, HTMLResponse
from liulianmao import ask


const_model_mapping = {
    "gpt-3-turbo": "glm-4",
    "gpt-4": "glm-4-0520",
    "gpt-4o": "glm-4v",
    "text-embedding-ada-002": "embedding-3",
}

app = FastAPI()


def forward_chat(request: Request):
    try:
        body = request.json()
        model = body.get("model")
        input_text = body.get("input")

        if model in const_model_mapping:
            model = const_model_mapping[model]

        response = ask(msg=input_text, model=model)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def forward_embedding(request: Request):
    try:
        body = request.json()
        model = body.get("model")
        input_text = body.get("input")

        if model in const_model_mapping:
            model = const_model_mapping[model]

        response = ask(msg=input_text, model=model)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def hello():
    # this need to be replaced with a html file, read it and response it
    return "Hello, user!"


@app.post("/paas/v1/chat/completions")
async def pass_v1_chat_completions(request: Request):
    return forward_chat(request)


@app.post("/paas/v4/chat/completions")
async def pass_v4_chat_completions(request: Request):
    return forward_chat(request)


@app.post("/embedding")
async def create_embedding(request: Request):
    return forward_embedding(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
