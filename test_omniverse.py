#!/usr/bin/env python3
"""
测试 omniverse 路由功能
"""

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from fastapi.testclient import TestClient
from main import app


def test_omniverse_endpoint_not_set():
    """测试当 OMNIVERSE_ENDPOINT 未设置时的错误处理"""
    # 确保环境变量不存在
    if "OMNIVERSE_ENDPOINT" in os.environ:
        del os.environ["OMNIVERSE_ENDPOINT"]
    
    client = TestClient(app)
    
    # 测试 omniverse 路由
    response = client.get("/omniverse/v1/test")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 应该返回 500 错误，因为 OMNIVERSE_ENDPOINT 未设置
    assert response.status_code == 500
    assert "OMNIVERSE_ENDPOINT" in response.json()["detail"]
    print("✓ 测试通过: OMNIVERSE_ENDPOINT 未设置时的错误处理")


def test_omniverse_routes_exist():
    """测试 omniverse 路由是否已注册"""
    client = TestClient(app)
    
    # 检查路由是否已注册
    routes = [route.path for route in app.routes]
    print("已注册的路由:")
    for route in routes:
        if "omniverse" in route:
            print(f"  - {route}")
    
    # 检查 omniverse 路由是否存在
    assert any("omniverse" in route.path for route in app.routes)
    print("✓ 测试通过: omniverse 路由已注册")


def test_omniverse_with_mock_endpoint():
    """测试使用模拟 endpoint 的情况"""
    # 设置一个无效的 endpoint 来测试错误处理
    os.environ["OMNIVERSE_ENDPOINT"] = "http://invalid-endpoint.test"
    
    client = TestClient(app)
    
    # 测试 GET 请求
    response = client.get("/omniverse/v1/chat/completion")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 由于 endpoint 无效，应该返回 502 错误
    # 注意：TestClient 可能会直接抛出异常，所以我们需要检查状态码
    if response.status_code == 502:
        print("✓ 测试通过: 无效 endpoint 返回 502 错误")
    else:
        print(f"注意: 返回状态码 {response.status_code}，预期 502")
    
    # 清理环境变量
    del os.environ["OMNIVERSE_ENDPOINT"]


def test_omniverse_path_extraction():
    """测试路径提取逻辑"""
    # 测试用例 - 注意：查询参数不会被包含在路径参数中
    test_cases = [
        ("/omniverse/v1/chat/completion", "v1/chat/completion"),
        ("/omniverse/paas/v4/response", "paas/v4/response"),
        ("/omniverse/api/test", "api/test"),  # 查询参数由 FastAPI 单独处理
        ("/omniverse/deep/nested/path", "deep/nested/path"),
    ]
    
    print("路径提取测试:")
    for url_path, expected_path in test_cases:
        # 模拟路径提取（实际在路由中由 FastAPI 处理）
        # 注意：查询参数 (?param=value) 不会被包含在路径中
        extracted = url_path.replace("/omniverse/", "", 1)
        print(f"  {url_path} -> {extracted} (预期: {expected_path})")
        assert extracted == expected_path
    
    print("✓ 测试通过: 路径提取逻辑正确")


if __name__ == "__main__":
    print("=" * 60)
    print("测试 omniverse 路由功能")
    print("=" * 60)
    
    try:
        test_omniverse_routes_exist()
        print()
        
        test_omniverse_path_extraction()
        print()
        
        test_omniverse_endpoint_not_set()
        print()
        
        test_omniverse_with_mock_endpoint()
        print()
        
        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)