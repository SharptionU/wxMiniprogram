# 导入项目配置
from fastapi import FastAPI

from core.config import settings
# 导入应用初始化函数
from core.setup.app import create_app

# 创建FastAPI应用实例
app = create_app()

def show_routes(_app:FastAPI):
    for route in _app.routes:
        if hasattr(route, "methods"):
            print(f"HTTP Route: {route.methods}\t{route.path}")
        elif hasattr(route, "path"):
            print(f"Static/Mount Route: {route.path}")
# 如果直接运行此文件，则启动应用
if __name__ == "__main__":
    import uvicorn
    show_routes(app)
    # 使用配置中的参数启动uvicorn服务器
    uvicorn.run(
        "main:app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=settings.uvicorn.reload,
        reload_dirs=settings.uvicorn.reload_dirs,
        reload_includes=settings.uvicorn.reload_includes,
        reload_excludes=settings.uvicorn.reload_excludes,
        log_level=settings.uvicorn.log_level,
        workers=settings.uvicorn.workers
    )