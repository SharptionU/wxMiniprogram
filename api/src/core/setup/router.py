from fastapi import FastAPI

from core.config import settings
from views.routes import api_router


def init_router(app: FastAPI):
    """初始化路由"""
    # 注册API路由，并添加前缀
    app.include_router(api_router, prefix=settings.api_prefix)

    """初始化额外路由"""

    # 根路径接口
    @app.get("/", tags=["根路径"])
    async def root():
        """
        根路径接口
        返回API服务的基本信息
        """
        return {
            "app_name": settings.name,
            "version": settings.version,
            "message": "欢迎使用山语户外电商平台API",
            "docs": f"{settings.api_prefix}/docs 或 {settings.api_prefix}/redoc"
        }

    # 健康检查接口
    @app.get("/health", tags=["系统"])
    async def health_check():
        """
        健康检查接口
        用于监控服务状态
        """
        return {"status": "ok", "version": settings.version}
    return app