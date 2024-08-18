# liulianmao-fastapi
A wrapper that can imitate forward gateway and make call use liulianmao


这玩意是配合[liulianmao](https://github.com/LaoshuBaby/liulianmao)使用的。

大部分时候当您需要转发API的时候，只需要用[one-api](https://github.com/songquanpeng/one-api)就可以了，剩下的时候用[new-api](https://github.com/Calcium-Ion/new-api)就可以了。

本项目主要适合如下场景

1. 为了更好的debug，需要更详细的日志
2. 为了对内容进行审计，需要更详细的日志
3. 需要对模型的名称或请求地址进行映射
4. 需要对模型的请求方法进行处理

## Usage Instructions

### Setting Up and Running the FastAPI Server

1. Install the required dependencies:
   ```bash
   pip install fastapi zhipuai
   ```

2. Create a file named `main.py` and add the following code:
   ```python
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
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Example Requests and Responses

#### Example Request

```json
{
    "model": "gpt-3-turbo",
    "input": "你好"
}
```

#### Example Response

```json
{
    "model": "glm-4",
    "data": [
        {
            "embedding": [
                -0.02675454691052437,
                0.019060475751757622,
                ...... 
                -0.005519774276763201,
                0.014949671924114227
            ],
            "index": 0,
            "object": "embedding"
        },
        ...
        {
            "embedding": [
                -0.02675454691052437,
                0.019060475751757622,
                ...... 
                -0.005519774276763201,
                0.014949671924114227
            ],
            "index": 2,
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
```
