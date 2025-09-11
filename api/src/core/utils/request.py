from schemas.base import BaseReqModel


def query_params_purify(m: BaseReqModel):
    q = m.dump_no_none()
    skip = q.pop('skip', 0)
    limit = q.pop('limit', 10)
    sort = q.pop('sort', None)
    _id = q.pop('id', None)

    if sort and sort.startswith('-'):
        sort = (sort[1:], -1)
    elif sort:
        sort = (sort, 1)

    query = {}
    for k in q:
        if isinstance(q[k], str):
            # 字符串包含查询，忽略大小写
            query[k] = {"$regex": q[k], "$options": "i"}
        else:
            query[k] = q[k]

    # 对 id查询
    if _id:
        query["_id"] = _id

    return query, skip, limit, sort
