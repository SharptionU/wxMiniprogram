"""日志打印中间件"""
import time
from starlette.middleware.base import BaseHTTPMiddleware, Request, Response, RequestResponseEndpoint
from core.config import settings

__all__ = ['LogMiddleware']


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,e:str="dev"):
        self.env = e
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print("use log middleware")
        start_time = time.time()
        # 开发环境下打印请求信息
        if self.env == "dev":
            # 打印请求信息
            print(f"\n{'=' * 50}")
            print(f"Request: {request.method} {request.url}")
            print(f"Headers: {dict(request.headers)}")

            # 尝试读取并打印请求体（非阻塞方式）
            try:
                body = await request.body()
                if body:
                    print(f"Body: {body.decode()}")
            except Exception:
                print("Body: [无法读取]")

        # 处理请求
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # 毫秒

        # 开发环境下打印响应信息
        if self.env == "dev":
            # 打印响应信息
            print(f"Response: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")

            # 尝试读取并打印响应体（非阻塞方式）
            try:
                body = response.body
                if body:
                    print(f"Body: {body.decode()}")
            except (AttributeError, UnicodeDecodeError):
                try:
                    # 对于流式响应
                    body_chunks = [chunk async for chunk in response.body_iterator]
                    response.body_iterator = AsyncIteratorWrapper(body_chunks)
                    print(f"Body: {b''.join(body_chunks).decode(errors='replace')}")
                except Exception:
                    print("Body: [无法读取]")

            print(f"Process Time: {process_time:.2f}ms")
            print(f"{'=' * 50}\n")

        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response


# 用于重新构建响应体的辅助类
class AsyncIteratorWrapper:
    def __init__(self, chunks):
        self.chunks = iter(chunks)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.chunks)
        except StopIteration:
            raise StopAsyncIteration
