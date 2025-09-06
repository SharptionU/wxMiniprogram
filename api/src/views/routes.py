# app/api/v1/api.py
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List

# 1. 创建 API v1 版本的总路由实例
# 这个实例将作为所有 v1 子路由的“容器”，最终被挂载到主应用
api_router = APIRouter(
    prefix="",  # 此处前缀为空，因为主应用会添加 /api/v1（见 main.py）
    tags=["API v1 总览"],  # OpenAPI 文档中分组标签
    responses={
        # 全局响应模板：所有子路由可复用
        status.HTTP_404_NOT_FOUND: {
            "description": "资源不存在",
            "content": {"application/json": {"example": {"detail": "请求的资源未找到"}}}
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "服务器内部错误",
            "content": {"application/json": {"example": {"detail": "服务器处理请求时发生错误"}}}
        }
    }
)

# 2. 导入各业务模块的子路由（从同目录下的 users.py、items.py 等文件）
# 注意：子路由文件（如 users.py）中需创建独立的 APIRouter 实例（通常命名为 router）
from .user import router as user_router  # 用户模块路由
# 若有其他模块（如订单、支付），继续导入：
# from .orders import router as order_router
# from .payments import router as payment_router

# 3. 将子路由挂载到总路由，并指定模块级路径前缀
# 挂载后，子路由的实际路径 = 主应用前缀（/api/v1） + 此处 prefix + 子路由自身路径
api_router.include_router(
    user_router,
    prefix="/users",  # 用户模块路径前缀：/api/v1/users
    tags=["用户管理"],  # 覆盖子路由的 tags（或补充），用于 OpenAPI 文档分组
    # 可选：添加模块级依赖（如仅管理员可访问该模块）
    # dependencies=[Depends(get_current_superuser)]
)



# # 若有其他模块，继续挂载：
# api_router.include_router(
#     order_router,
#     prefix="/orders",
#     tags=["订单管理"]
# )

# 4. 添加 API v1 版本的根路径接口（可选，用于版本说明）
@api_router.get("/", response_model=Dict)
async def get_api_v1_overview():
    """
    API v1 版本总览
    返回当前版本支持的所有业务模块及接口前缀
    """
    return {
        "当前 API 版本": "v1",
        "基础路径": "/api/v1",
        "支持的模块及路径前缀": [
            "/users - 用户管理（创建、查询、更新、删除用户）",
            "/items - 物品管理（创建、查询、更新、删除物品）",
            # "/orders - 订单管理",  # 若有其他模块，补充说明
            # "/payments - 支付管理"
        ],
        "文档地址": "/docs 或 /redoc"
    }