from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动阶段：创建 MongoDB 客户端和数据库实例
    print("🔗 连接 MongoDB...")
    # 创建异步客户端
    app.state.mongo_client = AsyncIOMotorClient(str(settings.mongo.db_uri))
    # 获取数据库实例
    app.state.mongo_db = app.state.mongo_client[settings.mongo.db_name]
    # 测试连接（可选，确保连接成功）
    try:
        await app.state.mongo_db.command("ping")  # 发送 ping 命令验证连接
        print(f"✅ 成功连接到 MongoDB: {settings.mongo.db_name}")
    except Exception as e:
        # 连接失败时终止应用启动
        raise RuntimeError(f"❌ MongoDB 连接失败: {str(e)}") from e

    yield  # 应用开始处理请求

    # 关闭阶段：关闭 MongoDB 客户端
    print("🔌 关闭 MongoDB 连接...")
    app.state.mongo_client.close()  # 关闭客户端释放连接
    print("❌ MongoDB 连接已关闭")