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

#### 请求的接口：/hello

**请求**

请求体：以curl表达：

```json
curl -X GET http://localhost:9000/
```

**响应:**

```json
{
    "os": "posix",
    "platform": "linux",
    "version": "3.11.0",
    "environment_variables": {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        ...
    }
}
```

#### 请求的接口：/logs

**请求**

请求体：以curl表达：

```json
curl -X GET http://localhost:9000/logs
```

**响应:**

```json
{
    "logs": [
        "log1.txt",
        "log2.txt",
        ...
    ]
}
```

#### 请求的接口：/logs/{filename}

**请求**

请求体：以curl表达：

```json
curl -X GET http://localhost:9000/logs/log1.txt
```

**响应:**

```text
Log file content here...
```

#### 请求的接口：/paas/v1/chat/completions

**请求**

请求体：以curl表达：

```json
curl -X POST http://localhost:9000/paas/v1/chat/completions -H "Content-Type: application/json" -d '{
    "model": "gpt-3-turbo",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ]
}'
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

#### 请求的接口：/paas/v4/chat/completions

**请求**

请求体：以curl表达：

```json
curl -X POST http://localhost:9000/paas/v4/chat/completions -H "Content-Type: application/json" -d '{
    "model": "gpt-3-turbo",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ]
}'
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

#### 请求的接口：/embedding

**请求**

请求体：以curl表达：

```json
curl -X POST http://localhost:9000/embedding -H "Content-Type: application/json" -d '{
    "model": "text-embedding-ada-002",
    "input": "Hello, world!"
}'
```

**响应:**

```json
{
    "model": "embedding-3",
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

## 部署方法

### 在Zeabur上部署

1. 创建一个新的Zeabur项目。
2. 将代码库连接到Zeabur项目。
3. 配置Zeabur以使用Python 3.11环境。
4. 设置启动命令为 `uvicorn main:app --host 0.0.0.0 --port $PORT`。
5. 部署项目。

### 在AWS Lambda上部署

1. 创建一个新的AWS Lambda函数。
2. 将代码打包为zip文件并上传到Lambda。
3. 配置Lambda函数以使用Python 3.11运行时。
4. 设置Lambda函数的入口点为 `main.app`。
5. 配置API Gateway以触发Lambda函数。
6. 部署API Gateway。
