from datetime import datetime
from pydantic import AnyUrl, BaseModel, Field

from schema.base import BaseReqModel  # 假设BaseReqModel含分页字段：skip/limit/sort等


class SwiperBase(BaseModel):
    """轮播图公共基础模型（包含所有场景的公共字段）"""
    title: str | None = None
    description: str | None = None
    image_url: AnyUrl | None = None  # 图片链接
    goods_id: str | None = None
    is_active: bool | None = True  # 默认启用


class SwiperReq(BaseReqModel, SwiperBase):
    """轮播图查询模型（继承分页基础模型+公共字段，用于接口查询参数）"""
    id: str | None = None  # 支持按id查询


class SwiperRes(SwiperBase):
    """轮播图响应模型（用于接口返回数据，包含数据库生成的字段）"""
    id: str  # 响应中必须返回id
    created_at: datetime | None = Field(None, description="创建时间（数据库自动生成）")


class SwiperCreate(SwiperBase):
    """轮播图创建模型（用于创建新轮播图，明确必填字段）"""
    title: str  # 创建时标题必填（覆盖父类的可选定义）
    image_url: AnyUrl  # 创建时图片链接必填（覆盖父类的可选定义）
    goods_id: str  # 创建时关联商品ID必填（覆盖父类的可选定义）


class SwiperUpdate(SwiperBase):
    """轮播图更新模型（用于部分更新，所有字段均可选）"""
    created_at: datetime | None = None  # 允许更新创建时间（按需开放）
    # 其他字段继承自SwiperBase，保持可选性（更新时可只传需要修改的字段）


class SwiperDelete(SwiperBase):
    ...
