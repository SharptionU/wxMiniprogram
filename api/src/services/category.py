from schema.constant import COLLECTION as C


class CateService:
    @staticmethod
    async def get_cate_info_by_store_id(store_id, db):
        """根据店铺ID获取分类信息"""

        query = {"store_id": store_id}
        cate_info = await db.find(C.PRODUCT_CATEGORY, query={"is_active": True})

        # 展开一二级分类
        cate_dict = {i["id"]: i for i in cate_info if i["level"] == 1}
        for i in cate_info:
            if i["level"] == 2:
                cate_dict[i["parent"]]["children"].append(i)
        cate_list=[i for i in cate_dict.values()]
        # 对children按照order排序
        for i in cate_list:
            if i["children"]:
                i["children"] = sorted(i["children"], key=lambda x: x["order"])
        # 对cate_list按照order排序
        sorted_list=sorted(cate_list,key=lambda x:x["order"])
        return sorted_list