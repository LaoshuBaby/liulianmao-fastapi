from fastapi import FastAPI, Request, HTTPException
from zhipuai import ZhipuAI

app = FastAPI()
client = ZhipuAI(api_key="your api key")

@app.post("/embedding")
async def create_embedding(request: Request):
    try:
        body = await request.json()
        model = body.get("model")
        input_text = body.get("input")

        # Remap model names if necessary
        model_mapping = {
            "gpt-3-turbo": "glm-4"
        }
        if model in model_mapping:
            model = model_mapping[model]

        response = client.embeddings.create(
            model=model,
            input=input_text,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
