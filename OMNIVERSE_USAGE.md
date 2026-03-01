# Omniverse 统一代理接口

## 概述

Omniverse 接口是一个统一的代理接口，可以将所有以 `/omniverse/` 开头的请求转发到配置的目标 endpoint。这样无论使用哪家的模型 API，都不需要再编写具体的适配控制器。

## 功能特性

- **统一入口**: 所有请求通过 `/omniverse/` 前缀访问
- **路径保留**: 保留 `/omniverse/` 之后的完整路径
- **查询参数**: 完整保留所有查询参数
- **多方法支持**: 支持 GET、POST、PUT、DELETE、PATCH、OPTIONS、HEAD 等 HTTP 方法
- **请求头转发**: 自动转发请求头（排除 host、content-length 等）
- **错误处理**: 完善的错误处理和日志记录

## 配置方法

### 环境变量配置

设置 `OMNIVERSE_ENDPOINT` 环境变量来指定目标 endpoint：

```bash
# 设置 OpenAI API
export OMNIVERSE_ENDPOINT=https://api.openai.com

# 设置 Anthropic API
export OMNIVERSE_ENDPOINT=https://api.anthropic.com

# 设置本地测试 endpoint
export OMNIVERSE_ENDPOINT=http://localhost:8080
```

### 在运行脚本中配置

修改 `run.sh` 脚本或在启动时设置环境变量：

```bash
# 方法1: 直接设置环境变量
OMNIVERSE_ENDPOINT=https://api.openai.com ./run.sh

# 方法2: 在 run.sh 中添加
export OMNIVERSE_ENDPOINT=https://api.openai.com
```

## 使用示例

### 示例 1: OpenAI 兼容接口

**原始请求:**
```
POST http://localhost:9000/omniverse/v1/chat/completions
Content-Type: application/json
Authorization: Bearer sk-xxx

{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

**实际转发到:**
```
POST https://api.openai.com/v1/chat/completions
Content-Type: application/json
Authorization: Bearer sk-xxx

{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

### 示例 2: 智谱 AI 接口

**原始请求:**
```
POST http://localhost:9000/omniverse/paas/v4/chat/completions
Content-Type: application/json
Authorization: Bearer token123

{
  "model": "glm-4",
  "messages": [
    {"role": "user", "content": "你好！"}
  ]
}
```

**实际转发到:**
```
POST https://open.bigmodel.cn/api/paas/v4/chat/completions
Content-Type: application/json
Authorization: Bearer token123

{
  "model": "glm-4",
  "messages": [
    {"role": "user", "content": "你好！"}
  ]
}
```

### 示例 3: 带查询参数的 GET 请求

**原始请求:**
```
GET http://localhost:9000/omniverse/api/v1/models?limit=10&offset=0
Authorization: Bearer sk-xxx
```

**实际转发到:**
```
GET https://api.openai.com/api/v1/models?limit=10&offset=0
Authorization: Bearer sk-xxx
```

### 示例 4: 深度嵌套路径

**原始请求:**
```
GET http://localhost:9000/omniverse/deep/nested/api/v1/resource/subresource
```

**实际转发到:**
```
GET https://api.example.com/deep/nested/api/v1/resource/subresource
```

## 代码示例

### Python 客户端示例

```python
import requests

# 配置
OMNIVERSE_BASE_URL = "http://localhost:9000/omniverse"
TARGET_ENDPOINT = "https://api.openai.com"  # 实际转发目标

# 聊天请求
def chat_completion():
    url = f"{OMNIVERSE_BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-xxx"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 获取模型列表
def list_models():
    url = f"{OMNIVERSE_BASE_URL}/v1/models"
    headers = {
        "Authorization": "Bearer sk-xxx"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()
```

### cURL 示例

```bash
# OpenAI 聊天
curl -X POST http://localhost:9000/omniverse/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxx" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'

# 智谱 AI 聊天
curl -X POST http://localhost:9000/omniverse/paas/v4/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token123" \
  -d '{
    "model": "glm-4",
    "messages": [
      {"role": "user", "content": "你好！"}
    ]
  }'

# 获取模型列表（带查询参数）
curl "http://localhost:9000/omniverse/v1/models?limit=10&offset=0" \
  -H "Authorization: Bearer sk-xxx"
```

## 错误处理

### 常见错误码

- **500**: `OMNIVERSE_ENDPOINT` 环境变量未设置
- **502**: 目标 endpoint 无法访问或网络错误
- **504**: 请求超时（默认 60 秒）
- **其他**: 目标 endpoint 返回的错误码会原样返回

### 错误响应示例

```json
{
  "detail": "OMNIVERSE_ENDPOINT environment variable is not set. Please set OMNIVERSE_ENDPOINT to the target endpoint URL."
}
```

```json
{
  "detail": "Bad Gateway: [Errno -2] Name or service not known"
}
```

## 日志记录

Omniverse 接口会记录详细的日志信息：

- 请求转发信息（源 URL → 目标 URL）
- 查询参数
- 错误信息
- 超时情况

日志级别可以通过环境变量配置。

## 高级配置

### 超时设置

默认超时时间为 60 秒。可以在 `omniverse.py` 中修改：

```python
self.client = httpx.AsyncClient(
    timeout=httpx.Timeout(60.0),  # 修改超时时间
    follow_redirects=True,
)
```

### 请求头过滤

默认会过滤以下请求头：
- `host`
- `content-length`
- `connection`
- `accept-encoding`

可以在 `omniverse.py` 的 `headers_to_remove` 列表中添加或删除需要过滤的请求头。

## 注意事项

1. **Endpoint 配置**: 必须设置 `OMNIVERSE_ENDPOINT` 环境变量
2. **路径处理**: `/omniverse/` 前缀会被自动移除
3. **查询参数**: 会自动保留并转发
4. **请求体**: POST、PUT、PATCH 请求的请求体会完整转发
5. **性能**: 转发会增加一定的延迟，建议目标 endpoint 与代理服务器网络良好

## 与现有接口的兼容性

Omniverse 接口与现有的专用接口（如 `/v1/chat/completions`、`/paas/v4/chat/completions`）共存，不会影响现有功能。

用户可以根据需要选择：
- 使用专用接口：直接调用现有控制器
- 使用 Omniverse 接口：通过统一代理访问任意 endpoint