from fastapi import FastAPI
from core.config import settings

def init_static_files(app: FastAPI):
    """初始化静态文件服务"""
    # 配置静态文件服务
    from fastapi.staticfiles import StaticFiles
    app.mount(f"{settings.api_prefix}/static", StaticFiles(directory="static"), name="static")
    return app
