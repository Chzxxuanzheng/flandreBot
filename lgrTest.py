import httpx
import json
import asyncio

# API 配置
BASE_URL = "http://127.0.0.1:49500"
API_TOKEN = "123456"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# 同步发送私聊消息
def send_private_message(user_id):
    """同步发送私聊消息"""
    url = f"{BASE_URL}/api/send_private_message"
    
    data = {
        "user_id": user_id,
        "message": [
            {
                "type": "image",
                "data": {
                        'uri': 'file:///home/lee/Nas/hub/数据/图片/芙兰/normally/B890195107AFE057D98C22134786A3AB.jpg',
                        'sub_type': 'normal'
					}
            }
        ]
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"API 请求失败: {e}")
        return None

# 通用同步 API 调用函数
def call_api(endpoint, method="GET", data=None):
    """通用同步 API 调用函数"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        with httpx.Client() as client:
            if method.upper() == "GET":
                response = client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = client.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的 HTTP 方法: {method}")
            
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"API 请求失败: {e}")
        return None

# 使用示例
async def main():
    """异步主函数示例"""
    # 示例1: 异步发送私聊消息
    result = await send_private_message_async(2431149266)
    if result:
        print("异步消息发送成功:", result)
    
    # 示例2: 异步调用其他 API 端点
    # result = await call_api_async("/api/get_login_info", "GET")
    # if result:
    #     print("获取登录信息:", result)

if __name__ == "__main__":
    # 同步调用示例
    print("=== 同步调用示例 ===")
    result = send_private_message(2431149266)
    if result:
        print("同步消息发送成功:", result)
    
    # # 异步调用示例
    # print("\n=== 异步调用示例 ===")
    # asyncio.run(main())