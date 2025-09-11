from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def init_cors(app: FastAPI):
    """初始化CORS中间件"""
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源，生产环境应限制为特定域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有HTTP头
    )
    return app
