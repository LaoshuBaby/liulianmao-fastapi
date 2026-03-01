import os
from typing import Dict, Any, Optional

import httpx
from fastapi import Request, HTTPException
from fastapi.responses import Response
from loguru import logger


class OmniverseRouter:
    """
    Omniverse 路由处理器
    将所有以 /omniverse/ 开头的请求转发到配置的 endpoint
    """
    
    def __init__(self, endpoint: Optional[str] = None):
        """
        初始化 Omniverse 路由器
        
        Args:
            endpoint: 目标 endpoint 地址，例如 "https://api.openai.com"
                      如果为 None，则从环境变量 OMNIVERSE_ENDPOINT 读取
        """
        self.endpoint = endpoint or os.environ.get("OMNIVERSE_ENDPOINT")
        if not self.endpoint:
            raise ValueError(
                "OMNIVERSE_ENDPOINT environment variable is not set. "
                "Please set OMNIVERSE_ENDPOINT to the target endpoint URL."
            )
        
        # 确保 endpoint 以 / 结尾
        if not self.endpoint.endswith("/"):
            self.endpoint = self.endpoint + "/"
            
        logger.info(f"Omniverse router initialized with endpoint: {self.endpoint}")
        
        # 创建异步 HTTP 客户端
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0),  # 60秒超时
            follow_redirects=True,
        )
    
    async def forward_request(self, request: Request, path: str) -> Response:
        """
        转发请求到目标 endpoint
        
        Args:
            request: FastAPI 请求对象
            path: 目标路径（不包含 /omniverse/ 前缀）
            
        Returns:
            FastAPI 响应对象
        """
        # 构建目标 URL
        target_url = f"{self.endpoint}{path}"
        
        # 获取查询参数
        query_params = dict(request.query_params)
        
        # 获取请求头
        headers = dict(request.headers)
        
        # 移除一些不需要转发的头
        headers_to_remove = [
            "host",
            "content-length",  # 让 httpx 自动计算
            "connection",
            "accept-encoding",
        ]
        for header in headers_to_remove:
            headers.pop(header, None)
        
        # 获取请求体
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # 记录请求信息
        logger.info(
            f"Omniverse forwarding: {request.method} {request.url.path} -> {target_url}"
        )
        logger.debug(f"Query params: {query_params}")
        logger.debug(f"Headers: {{...}}")
        
        try:
            # 转发请求
            response = await self.client.request(
                method=request.method,
                url=target_url,
                params=query_params,
                headers=headers,
                content=body if body else None,
            )
            
            # 构建响应
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
            
        except httpx.TimeoutException:
            logger.error(f"Request timeout to {target_url}")
            raise HTTPException(status_code=504, detail="Gateway Timeout")
            
        except httpx.RequestError as e:
            logger.error(f"Request error to {target_url}: {e}")
            raise HTTPException(status_code=502, detail=f"Bad Gateway: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()


# 创建全局 omniverse 路由器实例
_omniverse_router: Optional[OmniverseRouter] = None


def get_omniverse_router() -> OmniverseRouter:
    """获取 omniverse 路由器实例（单例模式）"""
    global _omniverse_router
    if _omniverse_router is None:
        _omniverse_router = OmniverseRouter()
    return _omniverse_router


async def close_omniverse_router():
    """关闭 omniverse 路由器"""
    global _omniverse_router
    if _omniverse_router is not None:
        await _omniverse_router.close()
        _omniverse_router = None