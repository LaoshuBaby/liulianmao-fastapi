# liulianmao-fastapi
一个可以模仿转发网关并使用liulianmao进行调用的包装器


这玩意是配合[liulianmao](https://github.com/LaoshuBaby/liulianmao)使用的。

大部分时候当您需要转发API的时候，只需要用[one-api](https://github.com/songquanpeng/one-api)就可以了，剩下的时候用[new-api](https://github.com/Calcium-Ion/new-api)就可以了。

本项目主要适合如下场景

1. 为了更好的debug，需要更详细的日志
2. 为了对内容进行审计，需要更详细的日志
3. 需要对模型的名称或请求地址进行映射
4. 需要对模型的请求方法进行处理

## 使用说明

### 设置和运行FastAPI服务器

1. 安装所需的依赖项:
   ```bash
   pip install fastapi liulianmao
   ```

2. 创建一个名为`main.py`的文件，并添加以下代码:
   ```python
   from fastapi import FastAPI, Request, HTTPException
   from liulianmao import ask

   app = FastAPI()

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

           response = ask(msg=input_text, model=model)
           return response
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

3. 运行FastAPI服务器:
   ```bash
   uvicorn main:app --reload
   ```

### 示例请求和响应

#### 示例请求

```json
{
    "model": "gpt-3-turbo",
    "input": "你好"
}
```

#### 示例响应

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
