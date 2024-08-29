# liulianmao-fastapi
A wrapper that can imitate forward gateway and make call use liulianmao

## 芝士神马？

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

2. 运行FastAPI服务器:
   ```bash
   uvicorn main:app --reload
   ```

   或

   py main.py

### 示例请求和响应

#### 请求的接口：/xxx

**请求**

请求体：以curl表达：

```json
curl -X -H xxxxx:port
{
    "model": "gpt-3-turbo",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ]
}
```

**响应:**

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

#### 请求的接口：/xxx

#### 请求的接口：/xxx

#### 请求的接口：/xxx