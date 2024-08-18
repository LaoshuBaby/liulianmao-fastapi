from fastapi import FastAPI, Request, HTTPException
# from zhipuai import ZhipuAI

const_model_mapping = {
            "gpt-3-turbo": "glm-4"
        }

app = FastAPI()
# client = ZhipuAI(api_key="your api key")

def forward_chat():
    pass

def forward_embedding():
    pass

@app.get("/")
async def hello():
    # return a hello page from read index.html
    pass

@app.post("/paas/v1/chat/completions"):
async def pass_v1_chat_completions():
    forward()

@app.post("/paas/v4/chat/completions"):
async def pass_v4_chat_completions():
    forward()

# v1 and v4 that will call https://open.bigmodel.cn/api/paas/v4/embeddings

# need to use forward_embedding

@app.post("/embedding")
async def create_embedding(request: Request):
    try:
        body = await request.json()
        model = body.get("model")
        input_text = body.get("input")

        # Remap model names if necessary

        if model in const_model_mapping:
            model = const_model_mapping[model]

        # response = client.embeddings.create(
        #     model=model,
        #     input=input_text,
        # )
        response={}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
