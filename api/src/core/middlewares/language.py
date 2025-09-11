"""获取语言中间件"""
import i18n
from starlette.middleware.base import BaseHTTPMiddleware, Request, Response, RequestResponseEndpoint
from core.config import settings

default_lang = settings.language.default


class LanguageMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 从请求头获取语言偏好（如 "en-US,en;q=0.9,zh-CN;q=0.8"）
        print("use lang middleware")
        accept_language = request.headers.get("Accept-Language", "")
        # 提取主要语言（取第一个分隔的语言，如 "en" 或 "zh"）
        locale = accept_language.split(",")[0].split("-")[0] if accept_language else default_lang

        # 检查语言是否在支持列表中，否则用默认语言
        supported_locales = ["zh", "en"]
        if locale not in supported_locales:
            locale = default_lang

        # 设置当前语言
        i18n.set("locale", locale)

        # 处理请求
        response = await call_next(request)
        return response
