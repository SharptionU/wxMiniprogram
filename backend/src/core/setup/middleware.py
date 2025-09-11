from fastapi import FastAPI

from core.middlewares.auth import AuthMiddleware
from core.middlewares.language import LanguageMiddleware
from core.middlewares.log import LogMiddleware


def init_middlewares(app: FastAPI):
    """"""
    """初始化所有中间件"""
    """洋葱模型，add_middleware的顺序决定了中间件的执行顺序 
       add 添加方式是压栈，因此最后压栈的中间件在请求到达路由前，是最先执行的"""
    # 添加语言中间件
    app.add_middleware(LanguageMiddleware)

    # 添加认证中间件，并配置无需认证的路径
    app.add_middleware(
        AuthMiddleware,
        exclude=[
            "login",  # 登录接口
            "register",  # 注册接口
            "captcha",  # 验证码接口
            "reset-password"  # 重置密码接口
        ],
        exclude_start=[
            "docs",  # 文档路径
            "static",  # 静态文件
            "openapi.json",  # OpenAPI规范
            "redoc"  # ReDoc文档
        ]
    )

    # 添加日志中间件
    app.add_middleware(LogMiddleware)
    return app