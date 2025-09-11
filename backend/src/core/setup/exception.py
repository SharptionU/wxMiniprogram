from fastapi import FastAPI

from core.exceptions import *


def init_exception_handler(app: FastAPI):
    """初始化异常处理器"""
    from fastapi import status, Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(UserNotExist)
    async def user_not_exist_handler(request: Request, exc: UserNotExist):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "用户不存在"}
        )

    @app.exception_handler(UserAlreadyExist)
    async def user_already_exist_handler(request: Request, exc: UserAlreadyExist):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "用户已存在"}
        )

    @app.exception_handler(UserNotAuthorized)
    async def user_not_authorized_handler(request: Request, exc: UserNotAuthorized):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "用户未授权"}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 记录异常信息（实际应用中应使用日志系统）
        print(f"未捕获的异常: {str(exc)}")
        import traceback
        traceback.print_exc()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "服务器内部错误"}
        )

    return app
