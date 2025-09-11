from datetime import datetime

from pydantic import BaseModel


class BaseReqModel(BaseModel):
    skip: int | None = 0
    limit: int | None = 10
    sort: str | None = "created_at"

    def dump(self):
        data = self.model_dump()
        return {k: data[k] for k in data if data[k] is not None}


class BaseUpdateModel(BaseModel):
    title: str | None = None
    description: str | None = None
    update_at: datetime | None = None

    def dump(self):
        data = self.model_dump()
        return {k: data[k] for k in data if data[k] is not None}


class BaseCreateRespModel(BaseModel):
    code: int
    msg: str
    id: str | None = None
