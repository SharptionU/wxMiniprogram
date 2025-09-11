"""api接口 jwt认证中间件"""
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, Request, Response, RequestResponseEndpoint
from fastapi.responses import JSONResponse
from core.auth.mjwt import parse_jwt
from core.config import settings


# 认证中间件
class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, exclude=None, exclude_start=None):
        super().__init__(app)
        self.exclude = exclude or []
        self.exclude_start = exclude_start or []

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint, *args,
                       **kwargs) -> Response:

        # 跳过不需要认证的路径，例如登录接口
        # [7:] 跳过 /api/v1
        print("use auth middleware")
        len_prefix =len(settings.api_prefix)+1
        if request.url.path[len_prefix:] in self.exclude:
            return await call_next(request)

        for start in self.exclude_start:
            if request.url.path[len_prefix:].startswith(start):
                return await call_next(request)

        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "authorization failed"})

        # 提取并验证令牌（实际应用中应替换为真实的令牌验证逻辑）
        token = auth_header.split(" ")[1]
        _ctt = parse_jwt(token)

        if not _ctt:
            return JSONResponse(
                content={"msg": "invalid token"},
                status_code=status.HTTP_401_UNAUTHORIZED)

        # 将用户信息挂载到request.state
        request.state.jwt_info = _ctt

        request.state.username = _ctt.get("username", "__anonymous__")
        request.state.unionID = _ctt.get("unionID", None)

        # 继续处理请求
        response = await call_next(request)
        return response
