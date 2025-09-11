def object_id_serializable(item: dict) -> dict:
    """
    将 MongoDB 的 _id 转换为字符串
    :param item:
    :return:
    """

    if isinstance(item, dict) and item.get("_id"):
        item["id"] = str(item.pop("_id"))  # ObjectId转字符串
    return item


def clear_field(data: dict, field: list[str] | str, keep_null: bool = False) -> dict:
    """
    清除不能或不想返回的字段
    :param data:
    :param field:
    :param keep_null: 对于清除的字段，替换为null,
    :return:
    """
    if isinstance(field, str):
        field = [field]
    for f in field:
        try:
            _ = data[f]
            if keep_null:
                data[f] = None
            else:
                data.pop(f)
        except KeyError:
            if keep_null:
                data[f] = None
            continue
    return data
