import re
from fastapi import APIRouter, Depends, HTTPException
from typing import Type, TypeVar
from pydantic import BaseModel

from depends.database import get_db_op
from depends.locale import gettext_translator
from depends.permission import require_permissions

from core.utils import query_params_purify

T = TypeVar('T', bound=BaseModel)


class ModelView:
    def __init__(self, model: Type[T], prefix: str = None, perm_dict=None, use_default_perm_rule=False):
        self.model = model
        self.table = re.sub('([a-z0-9])([A-Z])', r'\1_\2', model.__name__).lower()
        self.prefix = prefix or re.sub('([a-z0-9])([A-Z])', r'\1-\2', model.__name__).lower()
        if not perm_dict and use_default_perm_rule:
            perm_dict = {k: [f"{self.table}:{k}"] for k in ("list", "create", "update", "delete")}
        self.perm_dict = perm_dict or {}

        self.router = APIRouter(prefix=f"/{self.prefix}", tags=[self.prefix or self.model.__name__])

        self._register_routes()

    def _register_routes(self):

        l_req = self.model.get_list_request_model()
        l_res = self.model.get_list_response_model()
        u_req = self.model.get_update_request_model()
        u_res = self.model.get_update_response_model()
        c_req = self.model.get_create_request_model()
        c_res = self.model.get_create_response_model()
        d_res = self.model.get_delete_response_model()

        p_l = self.perm_dict.get("list")
        p_u = self.perm_dict.get("update")
        p_c = self.perm_dict.get("create")
        p_d = self.perm_dict.get("delete")

        # 查询接口
        @self.router.get("",
                         response_model=list[l_res],
                         dependencies=[require_permissions(p_l)])
        async def list_item(q: l_req = Depends(l_req),
                            db: get_db_op = Depends()):
            query, skip, limit, sort = query_params_purify(q)
            res = await db.find(self.table, query, skip=skip, limit=limit, sort=sort)
            return res

        # 创建接口
        @self.router.post("",
                          response_model=c_res,
                          dependencies=[require_permissions(p_c)])
        async def create_item(item: c_req,
                              _: gettext_translator = Depends(),
                              db: get_db_op = Depends()):
            item = self.model(**item.model_dump())
            res = await db.insert_one(self.table, item.mongo_dict())
            if res:
                return {
                    "code": 200,
                    "msg": _("create success"),
                    "id": str(res.inserted_id)
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=_("create failed")
                )

        # 详情接口
        @self.router.get("/{id}",
                         response_model=l_res,
                         dependencies=[require_permissions(p_l)])
        async def item_detail(id: str,
                              _: gettext_translator = Depends(),
                              db: get_db_op = Depends()):
            item = db.find_one(self.table, {"_id": id})
            if not item:
                raise HTTPException(status_code=404, detail=_("object not exist"))
            return item

        # 更新接口
        @self.router.put("/{id}",
                         response_model=u_res,
                         dependencies=[require_permissions(p_u)])
        async def update_item(id: str,
                              item: u_req,
                              _: gettext_translator = Depends(),
                              db: get_db_op = Depends()):
            update_data = item.model_dump(exclude_unset=True)

            if not update_data:
                raise HTTPException(
                    status_code=400,
                    detail=_("invalid update data"))
            res = await db.find_one_and_update(self.table, {"_id": id}, {"$set": update_data})

            if not res:
                raise HTTPException(
                    status_code=404,
                    detail=_("object not exist")
                )
            return res

        # 删除接口
        @self.router.delete("/{id}",
                            response_model=d_res,
                            dependencies=[require_permissions(p_d)])
        async def delete_item(id: str,
                              _: gettext_translator = Depends(),
                              db: get_db_op = Depends()):
            res = await db.delete_one(self.table, {"_id": id})
            if res.deleted_count == 1:
                return {
                    "code": 200,
                    "msg": _("delete success"),
                    "deleted_count": res.deleted_count}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=_("delete failed")
                )
