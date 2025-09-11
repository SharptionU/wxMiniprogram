from schema.constant import COLLECTION as C


class ProductService:
    """商品服务类"""
    @staticmethod
    async def get_product_by_store_and_cate(store_id=None,category_id=None, db=None):
        query={"is_active":True}
        if store_id:
            query["store_id"]=store_id
        if category_id:
            query["category_id"]=category_id
        return await db.find(C.PRODUCT,query,sort=("order", 1))
