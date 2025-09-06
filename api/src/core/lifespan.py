from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

# 1. 配置 MongoDB 连接信息
MONGODB_URI = "mongodb://localhost:27017"  # MongoDB 连接地址
DATABASE_NAME = "fastapi_mongo_demo"  # 数据库名称


# 2. 定义 lifespan 管理 MongoDB 连接生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动阶段：创建 MongoDB 客户端和数据库实例
    print("🔗 连接 MongoDB...")
    # 创建异步客户端
    app.state.mongo_client = AsyncIOMotorClient(MONGODB_URI)
    # 获取数据库实例
    app.state.mongo_db = app.state.mongo_client[DATABASE_NAME]
    # 测试连接（可选，确保连接成功）
    try:
        await app.state.mongo_db.command("ping")  # 发送 ping 命令验证连接
        print(f"✅ 成功连接到 MongoDB: {DATABASE_NAME}")
    except Exception as e:
        # 连接失败时终止应用启动
        raise RuntimeError(f"❌ MongoDB 连接失败: {str(e)}") from e

    yield  # 应用开始处理请求

    # 关闭阶段：关闭 MongoDB 客户端
    print("🔌 关闭 MongoDB 连接...")
    app.state.mongo_client.close()  # 关闭客户端释放连接
    print("❌ MongoDB 连接已关闭")
