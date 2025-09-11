from fastapi import FastAPI

from core.config import settings
from core.setup.cors import init_cors
from core.setup.exception import init_exception_handler
from core.setup.lifespan import app_lifespan
from core.setup.middleware import init_middlewares
from core.setup.router import init_router
from core.setup.static import init_static_files


def create_app():
    # 创建FastAPI应用实例，包含lifespan参数
    app = FastAPI(
        title=settings.name,
        version=settings.version,
        description="山语户外电商平台API服务",
        docs_url=f"{settings.api_prefix}/docs",  # Swagger文档路径
        redoc_url=f"{settings.api_prefix}/redoc",  # ReDoc文档路径
        openapi_url=f"{settings.api_prefix}/openapi.json",  # OpenAPI规范路径
        lifespan=app_lifespan  # 应用生命周期管理
    )
    # 调用其他初始化函数
    app = init_cors(app)
    app = init_middlewares(app)
    app = init_router(app)
    app = init_static_files(app)
    app = init_exception_handler(app)

    return app



